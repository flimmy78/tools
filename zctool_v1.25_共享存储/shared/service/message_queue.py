#!/usr/bin/python
import threading 
import logging
from service.reset_event import ResetEvent

class MessageQueue(object):
    
    """
    usage:
    MessageQueue(callback_function):
    start():
    stop():
    putMessage(msg):
    insertMessage(msg):
    
    """
    class StatusEnum:
        stopped = 0
        running = 1
        stopping = 2
        
    min_threhold = 5
    max_threhold = 200
    max_batch = 200
    check_interval = 0.02##20ms
    max_message = 10000
    
    def __init__(self, callback, batch_call = False):
        self.max_message = 10000
        self.status = MessageQueue.StatusEnum.stopped
        self.status_lock = threading.RLock()
        ##block after create
        self.message_available = ResetEvent()   #threading.Event()
        self.message_queue = []
        self.message_lock = threading.RLock()
        self.main_thread = threading.Thread(target=self.dispathProcess)
        self.callback = callback
        self.batch_call = batch_call

    def start(self):        
        """
        start service
        """
        with self.status_lock:
            if MessageQueue.StatusEnum.stopped != self.status:
                return False
            self.status = MessageQueue.StatusEnum.running
            self.main_thread.start()
            return True
        

    def stop(self):
        """
        stop service
        """
        with self.status_lock:
            if MessageQueue.StatusEnum.stopped == self.status:
                return
            if MessageQueue.StatusEnum.running == self.status:
                self.status = MessageQueue.StatusEnum.stopping
                ##notify wait thread
                self.message_available.set()
        
        self.main_thread.join()
        with self.status_lock:
            self.status = MessageQueue.StatusEnum.stopped

    def dispathProcess(self):
        while MessageQueue.StatusEnum.running == self.status:
            ##wait for signal
            self.message_available.wait(self.check_interval)
            if MessageQueue.StatusEnum.running != self.status:
                ##double protect
                break
##            if self.message_available.isSet():
##                self.message_available.clear()
            if(0 == len(self.message_queue)):
                ##empty
                continue
            with self.message_lock:
                request_count = len(self.message_queue)
                if(0 == request_count):
                    ##empty
                    continue
                ##FIFO/pop front
                fetch_count = min(request_count, self.max_batch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.message_available.set()
                request_list = self.message_queue[:fetch_count]
                del self.message_queue[:fetch_count]
            if self.callback:                
                if self.batch_call:
                    self.callback(request_list)
                else:
                    ##single call
                    for request in request_list:                
                        self.callback(request)
        
    def putMessage(self, message):
        """
        put message into queue tail
        """
        with self.message_lock:
            length = len(self.message_queue)
            if length >= self.max_message:
                return False
            self.message_queue.append(message)
##            length += 1
##            if (length < self.min_threhold) or (length > self.max_threhold):
            self.message_available.set()
            return True
        
    def insertMessage(self, message):
        """
        put message into queue head
        """
        with self.message_lock:
            length = len(self.message_queue)
            if length >= self.max_message:
                return False
            self.message_queue.insert(0, message)
##            length += 1
##            if (length < self.min_threhold) or (length > self.max_threhold):
            self.message_available.set()
            return True

    def batchPut(self,message_list):
        """
        put message into queue tail
        """
        with self.message_lock:
            length = len(self.message_queue)
            if length >= self.max_message:
                return False
            self.message_queue.extend(message_list)
            self.message_available.set()
            return True
        
