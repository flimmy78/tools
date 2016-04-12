#!/usr/bin/python

import logging
import datetime
import io
import os.path
import os
import threading
import hashlib
from whisper import *

class Observer(object):
    def __init__(self):
        self.event = threading.Event()
        self.file_id = ""
        self.success = False

    def onTaskStart(self, task_id, task_type):
        print "task start, id %d, type %d"%(task_id, task_type)
    
    def onTaskProgress(self, task_id, task_type,
                       current, total, percent, speed):
        speed_in_mib = speed/1048576
        print "progress:id %d, %d / %d, %.1f %%, %.1f MiBps"%(
            task_id, current, total, percent, speed_in_mib)
    
    def onTaskSuccess(self, task_id, task_type, file_id):
        print "success:id %d, file '%s'"%(task_id, file_id)
        self.file_id = file_id
        self.success = True
        self.event.set()

    def onTaskFail(self, task_id, task_type):
        print "fail:id %d"%(task_id)
        self.event.set()

    def waitFinish(self):
        self.event.clear()
        self.event.wait()

def checkSum(filename):
    source_file = io.open(filename, "rb")
    reader = io.BufferedReader(source_file)
    m = hashlib.md5()
    
    buf_size = 64*1024    
    more_data = True
    
    while more_data:
        data = reader.read(buf_size)
        input_length = len(data)
        if 0 == input_length:
            ##eof
            more_data = False
            break
        m.update(data)
    return m.hexdigest()      
    

if __name__ == '__main__':
    """
    format:
    server
    test_whisper -s [server_ip]

    client
    test_whisper -c [client_ip] -s [server_ip] [port]
    """
    import sys
    arg_count = len(sys.argv)
    if arg_count < 3:
        print "invalid param %s"%sys.argv
        sys.exit(0)
    if "-s" == sys.argv[1]:
        if arg_count != 3:
            print "invalid param %s for server"%sys.argv
            sys.exit(0)
##    handler = logging.StreamHandler(sys.stdout)
        handler = logging.FileHandler("whisper_server.log", "w")
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        root = logging.getLogger()
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)
        
        receive_ip = sys.argv[2]
        receive_port = 10000
        receive_channel = 5
        server = Whisper(receive_ip, receive_channel, "./tmp", "whisper")
        server.initial()
        server.start()
        print "server started, listen address '%s:%d'"%(
            receive_ip, server.getControlPort())
        raw_input("press any key...")

        server.stop()
        sys.exit(0)
    
    elif "-c" == sys.argv[1]:
        ##test_whisper -c [client_ip] -s [server_ip] [port] [filename]
        if arg_count < 5:
            print "invalid param %s for client"%sys.argv
            sys.exit(0)        
##        handler = logging.StreamHandler(sys.stdout)
        handler = logging.FileHandler("whisper_client.log", "w")
        formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        root = logging.getLogger()
        root.addHandler(handler)
        root.setLevel(logging.DEBUG)

        channel = 5
        
        receive_ip = sys.argv[4]
        if arg_count > 5 :
            receive_port = int(sys.argv[5])
        else:
            receive_port = 10000
        send_ip = sys.argv[2]

        if arg_count > 6:
            send_file = sys.argv[6]
        else:
    ##        send_file = "mini"
    ##        send_file = "normal"
            send_file = "big"
    ##        send_file = "huge"

        if not os.path.exists(send_file):
            print "send file '%s' not exists"%(send_file)
            sys.exit(0)
        ##size&md5
        file_size = os.path.getsize(send_file)
        md5 = checkSum(send_file)
        print "file size %d byte(s), md5 '%s'"%(file_size,md5)
        root.info("file size %d byte(s), md5 '%s'"%(file_size,md5))
            
        observer = Observer()
            
        client = Whisper(send_ip, channel, "./tmp", "whisper")
        client.initial()
        client.setObserver(observer)
        client.start()
        print "client started, listen address '%s:%d', target '%s:%d'"%(
            send_ip, client.getControlPort(),
            receive_ip, receive_port)
        
        begin_time = datetime.datetime.now()
        file_id = client.attachFile(send_file)

        root.info("file '%s' attached to id '%s'"%(
            send_file, file_id))
        ##write test
        task_id = client.allocateWriteTask(file_id, receive_ip, receive_port)
        client.startWriteTask(task_id)
        
        observer.waitFinish()
        end_time = datetime.datetime.now()
        diff = end_time - begin_time
        elapse_seconds = diff.seconds + float(diff.microseconds)/1000000
        file_size = os.path.getsize(send_file)
        speed = (float(file_size)/ 1048576)/elapse_seconds
        root.info("write speed %.2f MiB"%(speed))
    
        ##read test
        remote_file_id = observer.file_id
        begin_time = datetime.datetime.now()
        read_task = client.allocateReadTask(remote_file_id, receive_ip, receive_port)
        client.startReadTask(read_task)
        observer.waitFinish()
        end_time = datetime.datetime.now()
        diff = end_time - begin_time
        elapse_seconds = diff.seconds + float(diff.microseconds)/1000000
        if observer.success:
            read_result = "read_result"
            client.fetchFile(observer.file_id, read_result)
            file_size = os.path.getsize(read_result)
            md5 = checkSum(read_result)
            speed = (float(file_size)/ 1048576)/elapse_seconds
            root.info("read speed %.2f MiB"%(speed))

            print "read file %d byte(s), md5 '%s'"%(file_size, md5)
            root.info("read file %d byte(s), md5 '%s'"%(file_size, md5))
    
        client.stop()
        sys.exit(0)
