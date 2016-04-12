#!/usr/bin/python
import threading
from datagram import *

class SendTask(object):    
    def __init__(self, task_id):
        self.task_id = task_id
        self.data = ""
        self.ip = ""
        self.port = 0
                
    def initial(self, content, remote_ip, remote_port):
        datagram = Datagram(content, self.task_id)
        ##must change seq before serialize
        self.data = datagram.toString()
        self.ip = remote_ip
        self.port = remote_port
        return True

    def getData(self):
        return self.data

    def getIP(self):
        return self.ip

    def getPort(self):
        return self.port
        
