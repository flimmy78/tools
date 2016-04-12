#!/usr/bin/python
import threading
import zlib
import random
import hashlib
import sys
import socket
import select
import logging
import traceback

from service.service_status import StatusEnum
from datagram import *
from endpoint_manager import *
from app_message import *
from transport_command import *
from send_task_manager import *
from dispatch_pool import *
from cached_pool import *
from service.reset_event import ResetEvent

if "win32" == sys.platform:
    from packet_handler_win import *
else:
    from packet_handler import *

class ChannelInfo(object):
    def __init__(self, index):
        self.index = index
        self.ip = ""
        self.port = 0
        self.socket = None
        
class DispatchEvent(object):
    type_message = 0
    type_connected = 1
    type_disconnected = 2
    def __init__(self):
        self.name = ""
        self.type = self.type_message
        self.session_id = 0
        self.message = None

class Transporter(object):
    
    """
    usage:

    function:
    
    isRunning():is transpoter running
    bind(address, start_port, port_range):bind to local socket
    start():
    stop():
    connect(remote_ip, remote_port):
    disconnect(session_id):
    sendMessage(session_id, message_list):
    

    """
    timeout_check_interval = 1
    max_timeout = 5
    max_retry = 2
    max_task = 10000
    max_queue = 50000
    
    def __init__(self, name, logger_name,
                 handler = None, 
                 socket_count = 1,
                 process_channel = 1,
                 notify_channel = 1,
                 max_datagram_size = 548):
        
        self.handler = handler
        self.name = name
        self.bound = False
        self.ip = ""
        self.port = 0
        
        ##server_key
        int_value = random.random()*10000000
        sha = hashlib.sha1()
        sha.update(str(int_value))
        self.server_key = sha.hexdigest()

        self.channel_lock    = threading.RLock()
        self.channel_index   = 0
        self.channels        = []
        self.socket_count    = socket_count
        self.process_channel = process_channel
        self.notify_channel  = notify_channel
        
        self.logger           = logging.getLogger(logger_name)
        self.endpoint_manager = EndpointManager()
        
        self.max_datagram_size = max_datagram_size
        self.max_message_size  = max_datagram_size - 20
        self.status            = StatusEnum.stopped
        self.status_mutex      = threading.RLock()

        self.serial_request_available = ResetEvent()            # threading.Event()       # self.serialProcess()
        self.serial_request           = []                      # list of tuple (session_id, list of AppMessage)
        self.serial_thread            = []
        self.serial_lock              = threading.Lock()

        self.package_request_available = ResetEvent()           # threading.Event()      # self.packageProcess()
        self.package_request           = []                     # list of tuple (remote_ip, remote_port, datagram_list), datagram means stringlized of ConnectRequest()
        self.package_thread            = []
        self.package_lock              = threading.Lock()

        self.unpackage_request_available = ResetEvent()         # threading.Event()    # self.unpackageProcess()
        self.unpackage_request           = []                   # content tuple of (packet, remote_ip, remote_port)
        self.unpackage_thread            = []
        self.unpackage_lock              = threading.Lock()

        self.process_request_available = ResetEvent()           # threading.Event()      # self.processProcess()
        self.process_request           = []                     # contain tuple of (address, instance of subclass of TransportCommand()) 
        self.process_thread            = []
        self.process_lock              = threading.Lock()

        self.notify_request_available = ResetEvent()            # threading.Event()       # self.notifyProcess()
        self.notify_request           = []
        self.notify_thread            = []
        self.notify_lock              = threading.Lock()

        for i in range(process_channel):
            self.serial_thread.append(threading.Thread(target = self.serialProcess))
            self.package_thread.append(threading.Thread(target = self.packageProcess))
            self.unpackage_thread.append(threading.Thread(target = self.unpackageProcess))
            self.process_thread.append(threading.Thread(target = self.processProcess))
            
        for i in range(notify_channel):
            self.notify_thread.append(threading.Thread(target = self.notifyProcess))

        self.packet_handler = None
        self.task_manager = SendTaskManager(self.max_task, self.max_timeout, self.max_retry)
        
        ##timeout check
        self.timeout_check_event  = threading.Event()
        self.timeout_check_thread = threading.Thread(target=self.timeoutCheckProcess)
        
    def isRunning(self):
        return (StatusEnum.running == self.status)

    def bind(self, address, start_port = 5600, port_range = 200):   
        buf_size = 2*1024*1024
        
        self.packet_handler = PacketHandler(address, start_port, self.socket_count, self.onPacketReceived, buf_size)
        if not self.packet_handler.initial():
            return False
        
        self.bound = True
        self.ip = address
        self.port = self.packet_handler.getDefaultPort()
        ports = self.packet_handler.getLocalPorts()
        self.logger.info("<Transporter>bind to '%s:%d' success, port list:%s"%(self.ip, self.port, ports))
        for index in range(len(ports)):
            port = ports[index]
            info = ChannelInfo(index)
            info.ip = address
            info.port = port
            self.channels.append(info)
        return True
        
    def getListenPort(self):
        if self.bound:
            return self.port
        else:
            return -1
        
    def start(self):
        with self.status_mutex:
            
            if StatusEnum.stopped != self.status:
                self.logger.error("<Transporter>start transporter fail, not in stop status")
                return False
            self.status = StatusEnum.running
            
            self.packet_handler.start()
            
            for i in range(self.process_channel):
                self.serial_thread[i].start()
                self.package_thread[i].start()
                self.unpackage_thread[i].start()
                self.process_thread[i].start()
                
            for i in range(self.notify_channel):
                self.notify_thread[i].start()

            self.timeout_check_event.clear()
            self.timeout_check_thread.start()
            self.logger.info("<Transporter>start transporter success")
            return True

    def stop(self):
        with self.status_mutex:
            if StatusEnum.stopped == self.status:
                return
            if StatusEnum.running == self.status:
                self.status = StatusEnum.stopping
                self.logger.info("<Transporter>stopping transporter...")
                self.disconnectAll()
                
                self.timeout_check_event.set()
                self.serial_request_available.set()
                self.package_request_available.set()
                self.unpackage_request_available.set()
                self.process_request_available.set()
                self.notify_request_available.set()
                
                self.packet_handler.stop()
                                                           

        self.timeout_check_thread.join()
        
        for i in range(self.process_channel):
            self.serial_thread[i].join()
            self.package_thread[i].join()
            self.unpackage_thread[i].join()
            self.process_thread[i].join()
            
        for i in range(self.notify_channel):
            self.notify_thread[i].join()
        
        with self.status_mutex:
            self.status = StatusEnum.stopped

        self.logger.info("<Transporter>transporter stopped")


    def connect(self, remote_name, remote_ip, remote_port):
        if self.endpoint_manager.isExists(remote_name):
            self.logger.error("<Transporter>connect fail, remote endpoint '%s' already exists"%(remote_name))
            return False
        
        session_id = self.endpoint_manager.allocate(remote_name)
        if -1 == session_id:
            self.logger.error("<Transporter>connect fail, can't allocate endpoint for endpoint '%s'"%(remote_name))
            return False   
             
        ##new session
        channel_id = session_id%(self.socket_count)
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint.initial(channel_id):
            self.logger.error("<Transporter>connect fail, can't initial endpoint")
            return False

        info = self.channels[channel_id]
        
        request = ConnectRequest()
        request.sender = session_id
        request.ip = info.ip
        request.port = info.port
        request.name = self.name
        
        ##client_key
        int_value = random.random()*10000000
        sha = hashlib.sha1()
        sha.update(str(int_value))
        request.client_key = sha.hexdigest()

        datagram = request.toString()
        
        self.sendDatagram(remote_ip, remote_port, [datagram])
        return True

    def disconnect(self, session_id):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            self.logger.error("<Transporter>disconnect fail, invalid session %d"%(
                                                                                  session_id))
            return
        request = DisconnectRequest()
        request.name = self.name
        request.session = endpoint.remote_session
        
##        self.logger.info("[%08X]send disconnect request to node '%s'"%(session_id, endpoint.remote_name))
        self.sendDatagramToSession(session_id, [request.toString()])

    def disconnectAll(self):
        session_list = self.endpoint_manager.getConnectedEndpoint()
        if 0 == len(session_list):
            return
        
        for session_id in session_list:
            self.disconnect(session_id)

##        self.logger.info("<Transporter>disconnect %d connectd endpoint"%(len(session_list)))
        
        
    def sendMessage(self, session_id, message_list):
        with self.serial_lock:
            if self.max_queue < len(self.serial_request):
                self.logger.error("<Transporter>send message fail, send queue is full")
                return False
            self.serial_request.append((session_id, message_list))
            self.serial_request_available.set()
            return True
        
    def serialProcess(self):
        max_fetch = 100
        while self.isRunning():
            
            ##wait for signal
            self.serial_request_available.wait()
            if not self.isRunning():
                ##double protect
                ##pass notify to other thread
                self.serial_request_available.set()
                break   

            with self.serial_lock:
                ##check queue
                request_count = len(self.serial_request)
                if 0 == request_count:
                    ##empty
                    continue
                
                ##FIFO/pop front
                fetch_count = min(request_count, max_fetch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.serial_request_available.set()
                    
                request_list = self.serial_request[:fetch_count]
                del self.serial_request[:fetch_count]

            ##begin process
            try:
                ##list of (ip, port, datagram_list)
                package_request = []
                
                ##list of (session_id, message_list)
                for request in request_list:
                    session_id   = request[0]
                    message_list = request[1]
                    endpoint = self.endpoint_manager.getSession(session_id)
                    if not endpoint:
                        self.logger.error("<Transporter>send message fail, invalid session %d"%session_id)
                        continue
                    if not endpoint.isConnected():
                        self.logger.error("[%08X]send message fail, session disconnected"%session_id)
                        continue
                    begin_serial, end_serial = endpoint.allocateSerial(len(message_list))
                    if 0 == begin_serial:
                        self.logger.error("[%08X]send message fail, allocate serial fail"%session_id)
                        continue
                    
                    message_serial = begin_serial
                    datagram_list = []
                    for message in message_list:
                        content = message.toString()
                        if len(content) > self.max_message_size:
                            ##split
                            length = len(content)
                            total = (length - length % self.max_message_size)/self.max_message_size + 1
                            begin = 0
                            end = begin + self.max_message_size
                            index = 1
                            while begin != len(content):
                                message_data = MessageData()
                                message_data.serial = message_serial
                                message_data.index = index
                                message_data.total = total
                                message_data.data = content[begin:end]
                                message_data.session = endpoint.remote_session
                                
                                datagram_list.append(message_data.toString())                 
                                
                                ##next split
                                index += 1
                                begin = end
                                end = begin + self.max_message_size
                                if end > len(content):
                                    end = len(content)            
                                
                        else:
                            ##single datagram
                            message_data = MessageData()
                            message_data.serial = message_serial
                            message_data.index = 1
                            message_data.total = 1
                            message_data.data = content
                            message_data.session = endpoint.remote_session
                            datagram_list.append(message_data.toString())
                                    
                        if message_serial > EndpointSession.max_serial:
                            message_serial = 1
                        else:
                            message_serial += 1
                            
                    package_request.append((endpoint.nat_ip, endpoint.nat_port, datagram_list))
                ##end of for request in request_list:
                self.putToPackage(package_request)
                    
            except Exception as e:
                self.logger.exception("<Transporter>exception when serial message, message:%s" % (e.args))
                
    def putToPackage(self, request_list):
        """
        @request_list: list of tuple (remote_ip, remote_port, datagram_list)
        @datagram_list: list of datagram, datagram means stringlized of ConnectRequest(), MessageData(), 
        """
        with self.package_lock:
            if self.max_queue < len(self.package_request):
                self.logger.error("<Transporter>put package fail, package queue is full")
                return False
            self.package_request.extend(request_list)
            self.package_request_available.set()
            return True 

    def packageProcess(self):
        max_fetch = 100
        while self.isRunning():
            ##wait for signal
            self.package_request_available.wait()
            if not self.isRunning():
                ##double protect
                ##pass notify to other thread
                self.package_request_available.set()
                break  

            with self.package_lock:
                ##check queue
                request_count = len(self.package_request)
                if 0 == request_count:
                    ##empty
                    continue
                
                ##FIFO/pop front
                fetch_count = min(request_count, max_fetch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.package_request_available.set()
                    
                request_list = self.package_request[:fetch_count]
                del self.package_request[:fetch_count]

            ##package
            send_list = []##list of (packet, ip, port)

            ##key = (ip, port), value = datagram_list
            rawdata = {}
            ##list of (ip, port, datagram_list)
            ##resort by address
            for request in request_list:
                address = (request[0], request[1])                
                datagram_list = request[2]
                if not rawdata.has_key(address):
                    rawdata[address] = datagram_list
                else:
                    rawdata[address].extend(datagram_list)

            ##package to packet
            packets = {}
            for address in rawdata.keys():
                packets[address] = []
                cache = ""
                length = 0
                for data in rawdata[address]:
                    ##4 bytes length + raw data
                    data_length = len(data)
                    if (data_length + length) > self.max_datagram_size:
                        ##new packet, flush cache
                        if 0 != length:
                            packets[address].append(cache)
                        cache = data
                        length = data_length
                    else:
                        cache += data
                        length += data_length
                        
                if 0 != len(cache):
                    ##flush last packet
                    packets[address].append(cache)

            ##end of for address in rawdata.keys():

            ##resort to send_list
            for address in packets.keys():
                ip   = address[0]
                port = address[1]
                for packet in packets[address]:
                    send_list.append((packet, ip, port))

            packet_count = len(send_list)
            id_list = self.task_manager.allocate(packet_count)
            if 0 == len(id_list):
                self.logger.error("<Transporter>package fail, allocate %d task fail"%(packet_count))
                continue
            
            updated = self.task_manager.update(id_list, send_list)
            if updated != packet_count:
                self.logger.error("<Transporter>package fail, not all task updated (%d / %d)"%(updated, packet_count))
                self.task_manager.deallocate(id_list)
                continue
            
            ##refetch packeted data gram
            send_list = self.task_manager.fetch(id_list)
            
            if not self.packet_handler.sendPacketList(send_list):
                self.logger.error("<Transporter>package fail, send packet to handler fail")
                self.task_manager.deallocate(id_list)                
            
            
    def sendDatagramToSession(self, session_id, datagram_list):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            self.logger.error("<Transporter>send fail, invalid endpoint id %d"%(session_id))
            return False
        return self.sendDatagram(endpoint.nat_ip, endpoint.nat_port, datagram_list)
    
    def sendDatagram(self, remote_ip, remote_port, datagram_list):
        return self.putToPackage([(remote_ip, remote_port, datagram_list)])


    def onPacketReceived(self, message_list):
        """
        @message_list:list of (packet, remote_ip, remote_port)
        """
        with self.unpackage_lock:
            if self.max_queue < len(self.unpackage_request):
                self.logger.error("<Transporter>put unpackage fail, unpackage queue is full")
                return False
            self.unpackage_request.extend(message_list)
            self.unpackage_request_available.set()
            return True 

    def unpackageProcess(self):
        max_fetch = 100
        while self.isRunning():
            ##wait for signal
            self.unpackage_request_available.wait()
            if not self.isRunning():
                ##double protect
                ##pass notify to other thread
                self.unpackage_request_available.set()
                break
            
            with self.unpackage_lock:                
                ##check queue
                request_count = len(self.unpackage_request)
                if 0 == request_count:
                    ##empty
                    continue
                
                ##FIFO/pop front
                fetch_count = min(request_count, max_fetch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.unpackage_request_available.set()
                    
                request_list = self.unpackage_request[:fetch_count]
                del self.unpackage_request[:fetch_count]

            ##list of (address, datagram) 
            received_datagram = []          # contain tuple of (address, instance of subclass of TransportCommand()) 
            finished = []
            ack_packets = {}
            
            ##list of (packet, remote_ip, remote_port)
            for request in request_list:
                remote_ip   = request[1]
                remote_port = request[2]
                packet      = request[0]
                address = (remote_ip, remote_port)
                length = len(packet)
                begin = 0
                while (length - begin) >= 3:
                    header, seq = struct.unpack(">BH", packet[begin:(begin+3)])
                    if Datagram.header_mask != ((header&0xF0)>>4):
                        break
                    version = (header&0x0C)>>2
                    data_type = header&0x03
                    if 1 == data_type:
                        ##ack
                        finished.append(seq)                        
                        begin += 3
                    else:
                        ##data
                        if (length - begin) < 9:
                            ##incomplete
                            break
                        
                        data_length, crc = struct.unpack(">HI", packet[(begin+3):(begin+9)])
                        content_offset   = begin+9
                        data_content     = packet[content_offset:(content_offset + data_length)]
                        ##crc check
                        computed_crc = zlib.crc32(data_content)& 0xFFFFFFFF
                        if computed_crc != crc:
                            ##data damaged
                            break
                        ##unserialize
                        command_list = unpackageFromRawdata(data_content)
                        for command in command_list:
                            received_datagram.append((address, command))
                            
                        ack = DatagramACK(seq)                    
                        if not ack_packets.has_key(address):
                            ack_packets[address] = [ack.toString()]
                        else:
                            ack_packets[address].append(ack.toString())
                        
                        begin = content_offset + data_length                
                ##end while (length - begin) >= 3:
            ##end for request in request_list:
            if 0 != len(ack_packets):
                send_list = []##list of (packet, ip, port)
                ##send ack
                for address in ack_packets.keys():
                    ack_list = ack_packets[address]
                    for packet in ack_list:
                        send_list.append((packet, address[0], address[1]))

                if not self.packet_handler.sendPacketList(send_list):
                    self.logger.warn("<Transporter>try send %d ack fail!"%(len(send_list)))

            self.task_manager.deallocate(finished)
            self.putToProcess(received_datagram)
                
    def putToProcess(self, request_list):
        """
        @request_list: # contain tuple of (address, instance of subclass of TransportCommand()) 
        """
        ##list of (address, datagram)
        with self.process_lock:
            if self.max_queue < len(self.process_request):
                self.logger.error("<Transporter>put to process fail, process queue is full")
                return False
            self.process_request.extend(request_list)
            self.process_request_available.set()
            return True 

    def processProcess(self):
        max_fetch = 100
        while self.isRunning():
            ##wait for signal
            self.process_request_available.wait()
            if not self.isRunning():
                ##double protect
                ##pass notify to other thread
                self.process_request_available.set()
                break        

            with self.process_lock:
                ##check queue
                request_count = len(self.process_request)
                if 0 == request_count:
                    ##empty
                    continue
                
                ##FIFO/pop front
                fetch_count = min(request_count, max_fetch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.process_request_available.set()
                    
                request_list = self.process_request[:fetch_count]
                del self.process_request[:fetch_count]
            
            ##list of (address, datagram)       
            for request in request_list:    # contain tuple of (address, instance of subclass of TransportCommand()) 
                address = request[0]
                command = request[1]    
                try:
                    if command.type == TransportCommand.type_keep_alive:
                        self.handleKeepAlive(command, command.session)
                        
                    elif command.type == TransportCommand.type_connect_request:
                        self.handleConnectRequest(command, address, command.session)
                        
                    elif command.type == TransportCommand.type_connect_response:
                        self.handleConnectResponse(command, address, command.session)
                        
                    elif command.type == TransportCommand.type_connect_acknowledge:
                        self.handleConnectACK(command, command.session)
                        
                    elif command.type == TransportCommand.type_disconnect_request:
                        self.handleDisconnectRequest(command, command.session)
                        
                    elif command.type == TransportCommand.type_disconnect_response:
                        self.handleDisconnectResponse(command, command.session)
                        
                    elif command.type == TransportCommand.type_message_data:
                        self.handleMessageData(command, command.session)

                except Exception,ex:
                    self.logger.error("<Transporter>handle received datagram exception:%s"%(ex))
                    continue              

    def handleKeepAlive(self, msg, session_id):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            return
        if endpoint.remote_name != msg.name:
            self.logger.warn("<Transporter>recv keep alive with invalid name '%s'"%(msg.name))
            return        
        if endpoint.isDisconnected():            
            self.logger.warn("<Transporter>recv keep alive with disconnected session[%08X]"%(session_id))
            return
        endpoint.active()
    
    def handleConnectRequest(self, request, address, session_id):
        if 0 != len(request.digest):
            endpoint = self.endpoint_manager.getSession(session_id)
            if not endpoint:
                self.logger.error("<Transporter>accept connect request fail, invalid session %d"%(
                    session_id))
                return       
            
            ##verify dynamic key
            challenge_key = self.computeChallengeKey(request.client_key)
            verify_key = self.computeVerifyDigest(request.client_key, challenge_key)
            
            ##send response            
            response = ConnectResponse()
            if verify_key == request.digest:
                ##wait remote ack
                response.success = True
                response.name = self.name
                response.sender = session_id
                response.session = endpoint.remote_session
                self.sendDatagramToSession(session_id, [response.toString()])
                return
            else:
                response.success = False
                response.sender = session_id
                response.session = endpoint.remote_session

                self.logger.error("[%08X]connect reject, digest auth fail"%session_id)
                self.sendDatagramToSession(session_id, [response.toString()])
                self.endpoint_manager.deallocate(session_id)
                return
        else:            
            ##no digest
            remote_ip = request.ip
            remote_port = request.port
            if self.endpoint_manager.isExists(request.name):
                self.logger.error("<Transporter>recv connect request from '%s:%d', but endpoint '%s' already exist"%(
                                                                                                                     remote_ip, remote_port, request.name))
                return
                
                
            session_id = self.endpoint_manager.allocate(request.name)
            if -1 == session_id:
                self.logger.error("<Transporter>accept connect request fail, can't allocate session")
                return
            endpoint = self.endpoint_manager.getSession(session_id)
            channel_id = session_id%self.socket_count
            if not endpoint.initial(channel_id):
                self.logger.error("<Transporter>accept connect request fail, can't initial session")
                return
            endpoint.setRemoteAddress(request.sender, remote_ip, remote_port, address[0], address[1])
            
            response = ConnectResponse()
            response.success = False
            response.need_digest = True
            response.auth_method = 0##plain
            ##compute dynamic server key
            response.server_key = self.computeChallengeKey(request.client_key)
            response.client_key = request.client_key
            response.sender = session_id
            response.session = endpoint.remote_session
            ##allocated address
            channel_info = self.channels[channel_id]
            response.ip = channel_info.ip
            response.port = channel_info.port
            
            self.sendDatagram(endpoint.nat_ip, endpoint.nat_port, [response.toString()])    
                
    def handleConnectResponse(self, response, address, session_id):
        if not self.endpoint_manager.isAllocated(session_id):
            self.logger.error("<Transporter>accept connect response fail, invalid session %d"%(
                session_id))
            return
        if response.success:
            ##success
            endpoint = self.endpoint_manager.getSession(session_id)
            endpoint.setConnected()
            ##send connect ACK
            ack = ConnectAcknowledge()
            ack.name = self.name
            ack.session = endpoint.remote_session

            self.sendDatagramToSession(session_id, [ack.toString()])
            
##            self.logger.info("[%08X]connect success, remote name '%s'"%(session_id, endpoint.remote_name))
            self.notifySessionConnected(endpoint.remote_name, session_id)
            return
        elif not response.need_digest:
            ##auth fail
            self.logger.error("[%08X]connect request reject"%(session_id))
            self.endpoint_manager.deallocate(session_id)
            return
        else:
            ##need digest
            ##check local session
            challenge_key = response.server_key
            remote_session = response.sender
            nat_ip = address[0]
            nat_port = address[1]
##            self.logger.info("[%08X]connect request need disgest, challenge key '%s', remote session [%08X] (nat address '%s:%d')"%\
##                      (session_id, challenge_key, remote_session, nat_ip, nat_port))
            
            endpoint = self.endpoint_manager.getSession(session_id)
            ##update remote address
            endpoint.setRemoteAddress(remote_session, response.ip, response.port, nat_ip, nat_port)
          
            ##compute dynamic key
            verify_key = self.computeVerifyDigest(response.client_key, challenge_key)

            request = ConnectRequest()
            request.client_key = response.client_key
            request.digest = verify_key
            request.name = self.name
            request.sender = session_id
            request.session = endpoint.remote_session

            self.sendDatagramToSession(session_id, [request.toString()])
            
    def handleConnectACK(self, msg, session_id):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            self.logger.error("<Transporter>accept connect ack fail, invalid session %d"%(
                session_id))
            return
        endpoint.setConnected()
##        self.logger.info("[%08X]connect success, remote name '%s'"%(session_id, endpoint.remote_name))
        self.notifySessionConnected(endpoint.remote_name, session_id)
    
    def handleDisconnectRequest(self, msg, session_id):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            self.logger.error("<Transporter>accept disconnect request fail, invalid session %d"%session_id)
            return
        ##response
        response = DisconnectResponse()
        response.success = True
        response.session = endpoint.remote_session
        
        self.sendDatagramToSession(session_id, [response.toString()])
##        self.logger.info("[%08X]disconnect success, remote node '%s' removed"%(session_id, endpoint.remote_name))
        self.notifySessionDisconnected(endpoint.remote_name, session_id)
        self.endpoint_manager.deallocate(session_id)        
        
    def handleDisconnectResponse(self, msg, session_id):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            self.logger.error("<Transporter>accept disconnect response fail, invalid session %d"%session_id)
            return
        self.logger.info("[%08X]disconnect success, remote node '%s' removed"%(session_id, endpoint.remote_name))
        self.notifySessionDisconnected(endpoint.remote_name, session_id)
        self.endpoint_manager.deallocate(session_id)
        
    def handleMessageData(self, msg, session_id):
        endpoint = self.endpoint_manager.getSession(session_id)
        if not endpoint:
            self.logger.error("<Transporter>handle message data fail, invalid session %d"%session_id)
            return
        
        if 1 == msg.total:
            ##single data
            message = AppMessage.fromString(msg.data)
            
        else:
            ##multi data
            endpoint.cacheData(msg.serial, msg.index, msg.total, msg.data)
            if not endpoint.isCacheFinished(msg.serial):
                return
            ##finished
            content = endpoint.obtainCachedData(msg.serial)
            
            message = AppMessage.fromString(content)

##        self.logger.info("<Transporter>debug:recv message data, message id %d, type %d, session[%08X]"%(
##            message.id, message.type, message.session))
        self.notifyMessageReceived(message, session_id)


    def computeChallengeKey(self, client_key):
        number1 = zlib.crc32(client_key)&0xFF0F00FF
        number2 = zlib.crc32(self.server_key)&0xF0FFFF0F
        number3 = number1^number2
        sha = hashlib.sha1()
        sha.update(str(number3))
        return sha.hexdigest()
    
    def computeVerifyDigest(self, client_key, challenge_key):
        number1 = zlib.crc32(client_key)&0xFFFFF0FF
        number4 = zlib.crc32(challenge_key)&0xF0F0FFF0
        number5 = number1^number4
        sha = hashlib.sha1()
        sha.update(str(number5))
        return sha.hexdigest() 

    def notifyMessageReceived(self, message, session_id):
        event = DispatchEvent()
        event.type = DispatchEvent.type_message
        event.message = message
        event.session_id = session_id
        self.dispatch([event])
        
    def notifySessionConnected(self, remote_name, session_id):
##        self.debug("<SessionLayer>session connected, remote name '%s', id [%08X]"%(remote_name, session_id))
        event = DispatchEvent()
        event.type = DispatchEvent.type_connected
        event.name = remote_name
        event.session_id = session_id
        self.dispatch([event])

    def notifySessionDisconnected(self, remote_name, session_id):
##        self.debug("<SessionLayer>session disconnected, remote name '%s', id [%08X]"%(remote_name, session_id))
        event = DispatchEvent()
        event.type = DispatchEvent.type_disconnected
        event.name = remote_name
        event.session_id = session_id
        self.dispatch([event])
            
    def dispatch(self, event_list):
        with self.notify_lock:
            if self.max_queue < len(self.notify_request):
                self.logger.error("<Transporter>dispatch event fail, notify queue is full")
                return False
            self.notify_request.extend(event_list)
            self.notify_request_available.set()
            return True 

    def notifyProcess(self):
        max_fetch = 100
        while self.isRunning():
            ##wait for signal
            self.notify_request_available.wait()
            if not self.isRunning():
                ##double protect
                ##pass notify to other thread
                self.notify_request_available.set()
                break   

            with self.notify_lock:
                ##check queue
                request_count = len(self.notify_request)
                if 0 == request_count:
                    ##empty
                    continue
                
                ##FIFO/pop front
                fetch_count = min(request_count, max_fetch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.notify_request_available.set()
                    
                request_list = self.notify_request[:fetch_count]
                del self.notify_request[:fetch_count]
            
            if not self.handler:
                continue
            
            for event in request_list:
                if DispatchEvent.type_message == event.type:
                    self.handler.onMessageReceived(event.message, event.session_id)
                elif DispatchEvent.type_connected == event.type:
                    self.handler.onSessionConnected(event.name, event.session_id)
                elif DispatchEvent.type_disconnected == event.type:
                    self.handler.onSessionDisconnected(event.name, event.session_id)                    

    def timeoutCheckProcess(self):
        keep_alive_interval = 5
        keep_alive_counter = 0
        while self.isRunning():
            self.timeout_check_event.wait(self.timeout_check_interval)
            if not self.isRunning():
                ##service stopped
                break
            
            ##check task
            retry_list, remove_list = self.task_manager.checkTimeout()
            if 0 != len(retry_list):
                ##list of (packet, ip, port)
                send_list = self.task_manager.fetch(retry_list)
                    
                if not self.packet_handler.sendPacketList(send_list):
                    self.logger.warn("<Transporter>try resend %d packet(s) fail!"%(
                                                                                   len(send_list)))
                else:
                    self.logger.warn("<Transporter>resend %d packet(s)"%(
                                                                         len(retry_list)))
                    
            if 0 != len(remove_list):
                self.task_manager.deallocate(remove_list)
                self.logger.warn("<Transporter>deallocate %d failed packet(s)"%(
                                                                                len(remove_list)))
                    
            ##end for channel in range(self.socket_count):
            
            ##check endpoint session
            timeout_list = self.endpoint_manager.checkTimeout()
            for session_id in timeout_list:
                ##timeout session
                endpoint = self.endpoint_manager.getSession(session_id)
                self.notifySessionDisconnected(endpoint.remote_name, session_id)
                self.endpoint_manager.deallocate(session_id)

            keep_alive_counter = (keep_alive_counter + 1)%keep_alive_interval
            if 0 == keep_alive_counter:
                alive_list = self.endpoint_manager.getConnectedEndpoint()
                for session_id in alive_list:
                    ##alive session
                    endpoint = self.endpoint_manager.getSession(session_id)
                    
                    request = KeepAlive()
                    request.name = self.name
                    request.session = endpoint.remote_session                    
                    
                    self.sendDatagramToSession(session_id, [request.toString()])
                
            
