#!/usr/bin/python
import io
import os
import os.path
import logging
import threading
import binascii
from whisper_task import *
from whisper_command import *
from whisper_receiver import *
from whisper_sender import *

class WhisperWriteTask(WhisperTask):
    max_timeout = 100
    ##in seconds
    report_interval = 2
    def __init__(self, task_id, proxy):
        WhisperTask.__init__(self, task_id, TaskTypeEnum.write, proxy)
        self.reset()
        
    def allocate(self, file_id, filename, is_server,
                 file_size, block_size, strip_length,
                 remote_ip, remote_port):
        WhisperTask.allocate(self, file_id, filename, is_server)
        self.file_size = file_size
        self.block_size = block_size
        self.strip_length = strip_length
        self.remote_ip = remote_ip
        self.remote_port = remote_port 
        
    def setRemoteTask(self, task_id):
        with self.lock:
            self.remote_task  = task_id

    def setRemoteFile(self, file_id):
        with self.lock:
            self.remote_file = file_id

    def getRemoteFile(self):
        with self.lock:
            return self.remote_file
            
    def connect(self, max_channel):
        with self.lock:
            command = WriteCommand(self.task_id,
                                   self.file_size, self.block_size,
                                   self.strip_length, max_channel)
            return self.sendCommand(command, self.remote_ip, self.remote_port)

    def createReceiver(self):
        with self.lock:
            self.receiver = WhisperReceiver(self.filename, self.file_size, self.block_size, self.strip_length)
            return self.receiver.prepare()

    def createSender(self, port_list):
        with self.lock:
            self.sender = WhisperSender(self.filename, self.file_size, self.block_size, self.strip_length)
            self.remote_data_port = port_list
            self.remote_data_port_count = len(port_list)
            return self.sender.prepare(len(port_list) * 4)

    def startTransport(self):
        with self.lock:
            if self.sender is None:
                return False
            data_list = self.sender.fetchData(self.getWindowSize())
            request_list = []
            for data_block in data_list:
                data_size = len(data_block.data)
                crc = binascii.crc32(data_block.data)&0xFFFFFFFF
                remote_port = self.remote_data_port[(data_block.block%self.remote_data_port_count)]
                
                msg = Data(self.task_id, self.remote_task,
                           data_block.strip, data_block.block,
                           data_size, crc, data_block.data)
                request_list.append((msg, self.remote_ip, remote_port))
                
            self.sendData(request_list)
##            self.onStart()
            return True


    def handleData(self, command, sender_ip, sender_port):
        with self.lock:
            if self.receiver is None:
                return False
            self.counter = 0
            ##crc check
            crc = binascii.crc32(command.data)&0xFFFFFFFF
            if crc != command.crc:
                logging.warn("<Whisper>task[%d]:block %d.%d check sum fail"%(
                    self.task_id, command.strip_id, command.block_id))
                return False
            ##send ack first
            ack = DataAck(self.remote_task, command.strip_id, command.block_id)
            self.sendData([(ack, sender_ip, sender_port)])
    ##        logging.info("<Whisper>debug:block received, block %d"%(command.block_id))
            return self.receiver.writeData(command.strip_id, command.block_id, command.data)
            
    def handleDataAck(self, command, sender_ip, sender_port):
        with self.lock:
            if self.sender is None:
                return False
            self.counter = 0
            self.onDataAck()
            
            strip_id = command.strip_id
            block_id = command.block_id
            if not self.sender.complete(strip_id, block_id):
    ##            logging.error("<Whisper>task[%d]:can't complete block %d/%d"%(
    ##                self.task_id, strip_id, block_id))
                return False
    ##        logging.info("<Whisper>debug:block ack, block %d"%(block_id))
            if self.sender.isFinished():
                finish = Finish(self.task_id, self.remote_task)
                self.sendCommand(finish, self.remote_ip, self.remote_port)
                logging.info("<Whisper>task[%d]:finished, notify remote receiver"%(
                    self.task_id))
                return True
            data_list = self.sender.fetchData(self.getWindowSize())
            request_list = []
            for data_block in data_list:
                data_size = len(data_block.data)
                crc = binascii.crc32(data_block.data)&0xFFFFFFFF
                remote_port = self.remote_data_port[(data_block.block%self.remote_data_port_count)]
                
                msg = Data(self.task_id, self.remote_task,
                           data_block.strip, data_block.block,
                           data_size, crc, data_block.data)
                request_list.append((msg, self.remote_ip, remote_port))
    ##            logging.info("<Whisper>debug:send next block, send block %d"%(data_block.block))
                
            self.sendData(request_list)
            return True
                
    def handleFinish(self, command, sender_ip, sender_port):        
        with self.lock:
            if self.receiver is None:
                return False
            if self.receiver.isFinished():
                self.finished = True
                ack = FinishAck(self.remote_task)
                self.sendCommand(ack, self.remote_ip, self.remote_port)
                logging.info("<Whisper>task[%d]:receiver finished"%(
                    self.task_id))
                return True
            else:
                logging.info("<Whisper>task[%d]:recv finish event, but not all data received"%(
                    self.task_id))
                return False

    def handleFinishAck(self, command, sender_ip, sender_port):
        with self.lock:
            if self.sender is None:
                return False
            self.sender.close()
            self.finished = True
            self.success = True
            logging.info("<Whisper>task[%d]:sender finished"%(
                self.task_id))
##            self.onSuccess(self.remote_file)
            return True

    def check(self):
        with self.lock:
            self.counter += 1
            if self.counter > self.max_timeout:
                logging.info("<Whisper>task[%d]:task timeout fail"%(
                        self.task_id))
                self.finished = True
                self.success = False
##                self.onFail()
                return False            
            if (self.is_server) and (self.receiver):
                ##write server with receiver
                if not self.receiver.check():
                    ##check fail
                    logging.info("<Whisper>task[%d]:receiver check fail"%(
                        self.task_id))
                    self.finished = True
##                    self.onFail()
                    return False
                return True
            
            elif self.sender:
                ##write client with sender
                if self.sender.isFinished():
                    finish = Finish(self.task_id, self.remote_task)
                    self.sendCommand(finish, self.remote_ip, self.remote_port)
                    logging.info("<Whisper>task[%d]:notify remote receiver when check"%(
                        self.task_id))
                    return True
                retry_list, fail_list = self.sender.check()
                if 0 != len(fail_list):
                    ##send fail
                    logging.info("<Whisper>task[%d]:sender check fail"%(
                        self.task_id))
                    self.finished = True
##                    self.onFail()
                    return False
                elif 0 != len(retry_list):
                    lost = 0
                    ##retry
                    for cache_index in retry_list:
                        data_list = self.sender.fetchFailedData(cache_index)
                        lost += len(data_list)
                        request_list = []
                        for data_block in data_list:
                            data_size = len(data_block.data)
                            crc = binascii.crc32(data_block.data)&0xFFFFFFFF
                            remote_port = self.remote_data_port[(data_block.block%self.remote_data_port_count)]
                            
                            msg = Data(self.task_id, self.remote_task,
                                       data_block.strip, data_block.block,
                                       data_size, crc, data_block.data)
                            request_list.append((msg, self.remote_ip, remote_port))
    ##                        logging.warn("<Whisper>task[%d]:resend block %d"%(
    ##                            self.task_id, data_block.block))
                            
                        self.sendData(request_list)
    ##                logging.warn("<Whisper>task[%d]:resend %d lost block"%(
    ##                    self.task_id, lost))
                    self.onDataLost(lost)
                        
                ##check progress
                self.check_counter += 1
                self.check_counter = self.check_counter%(self.report_interval * 10)
                if 0 == self.check_counter:
                    sent_bytes, total_bytes, percentage, speed = self.sender.statistic()
                    self.processed = sent_bytes
                    self.total = total_bytes
                    self.progress = percentage
                    self.speed = speed
##                    self.onProgress(sent_bytes, total_bytes, percentage, speed)
                return True
