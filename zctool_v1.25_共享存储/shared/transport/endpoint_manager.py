#!/usr/bin/python
import datetime
import threading
from service.time_util import *
from endpoint_session import *

class EndpointManager(object):
    def __init__(self, max_capacity = 1024):
        self.lock = threading.RLock()
        self.max_capacity = max_capacity
        self.last_id = 0
        self.name_map = dict()
        self.session_map = dict()
        self.allocated_map = dict()
        for session_id in range(max_capacity):
            session = EndpointSession(session_id)
            self.session_map[session_id] = session
            self.allocated_map[session_id] = False

    def allocate(self, remote_name):
        with self.lock:
            if self.name_map.has_key(remote_name):
                return -1
            for offset in range(self.max_capacity):
                session_id = (self.last_id + offset + 1)% self.max_capacity
                if not self.allocated_map[session_id]:
                    ##unallocated
                    self.allocated_map[session_id] = True
                    self.session_map[session_id].allocate(remote_name)
                    self.name_map[remote_name] = session_id
                    self.last_id = session_id
                    return session_id
            return -1

    def deallocate(self, session_id):
        with self.lock:
            if(session_id >= self.max_capacity):
                return False
            if not self.allocated_map[session_id]:
                return False
            del self.name_map[self.session_map[session_id].getRemoteName()]
            self.allocated_map[session_id] = False
            self.session_map[session_id].deallocate()
            return True

    def getSession(self, session_id):
        with self.lock:
            if(session_id >= self.max_capacity):
                return None
            if not self.allocated_map[session_id]:
                return None
            return self.session_map[session_id]
    
    def isAllocated(self, session_id):
        with self.lock:
            if(session_id >= self.max_capacity):
                return False
            return self.allocated_map[session_id]
        

    def isExists(self, remote_name):
        with self.lock:
            return (self.name_map.has_key(remote_name))
    
    def checkTimeout(self):
        with self.lock:
            timeout_list = []
            for session_id in range(self.max_capacity):
                if self.allocated_map[session_id]:
                    if not self.session_map[session_id].check():
                        timeout_list.append(session_id)
                        
            return timeout_list

    def getConnectedEndpoint(self):
        with self.lock:
            result = []
            for session_id in range(self.max_capacity):
                if self.allocated_map[session_id]:
                    if self.session_map[session_id].isConnected():
                        result.append(session_id)

            return result

                
