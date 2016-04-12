#!/usr/bin/python
import service_status
import threading
import traceback
import datetime

from service_status import StatusEnum
from logger_helper import * 
from service.reset_event import ResetEvent

class BaseService(LoggerHelper):
    def __init__(self, logger_name, max_request = 10000):
        LoggerHelper.__init__(self, logger_name)
        self.__max_request = 10000
        self.__status = StatusEnum.stopped
        self.__status_mutex = threading.RLock()
        ##block after create
        self.__request_available = ResetEvent()   #threading.Event()
        self.__request_list = []
        self.__request_lock = threading.Lock()
        self.__main_thread = threading.Thread(target=self.__mainProcess)

    def start(self):        
        """
        start service
        """
        with self.__status_mutex:
            if StatusEnum.stopped != self.__status:
                return False
            if not self.onStart():
                return False
            self.__status = StatusEnum.running
            self.__main_thread.start()
            return True
        

    def stop(self):
        """
        stop service
        """
        with self.__status_mutex:
            if StatusEnum.stopped == self.__status:
                return
            if StatusEnum.running == self.__status:
                self.__status = StatusEnum.stopping
                ##notify wait thread
                self.__request_available.set()
        
        self.__main_thread.join()
        with self.__status_mutex:
            self.__status = StatusEnum.stopped
        self.onStop()

    def __mainProcess(self):
        max_batch = 100
        while StatusEnum.running == self.__status:
            ##wait for signal
            self.__request_available.wait()
            if StatusEnum.running != self.__status:
                ##double protect
                self.__request_available.set()
                break
            with self.__request_lock:
                request_count = len(self.__request_list)
                if(0 == request_count):
                    ##empty
                    continue
                ##FIFO/pop front
                fetch_count = min(request_count, max_batch)
                if fetch_count < request_count:                    
                    ##more available,self invoke
                    self.__request_available.set()
                    
                request_list = self.__request_list[:fetch_count]
                del self.__request_list[:fetch_count]

            
            try:
##                self.info("<BaseService>debug:%d request fetched"%(fetch_count))
                for request in request_list:
##                    begin = datetime.datetime.now()
                    
                    self.OnRequestReceived(request)
                    
##                    diff = datetime.datetime.now() - begin
##                    elapse_seconds = diff.seconds + float(diff.microseconds)/1000000
##                    if (request.type == 0) or(request.type == 1):
##                        ##message
##                        msg = request.message
##                        self.info("<BaseService>debug:handle message in %.1f second(s), msg type %d, id %d, session[%08X]"%(
##                            elapse_seconds, msg.type, msg.id, msg.session))
##                    else:
##                        ##
##                        self.info("<BaseService>debug:handle request in %.1f second(s), request type %d, session[%08X]"%(
##                            elapse_seconds, request.type, request.session_id))
                
            except Exception as e:
                self.console("<BaseService>OnRequestReceived exception:%s"%e.args[0])
                self.exception("<BaseService>OnRequestReceived exception:%s"%e.args[0])
                traceback.print_exc()
        
    def putRequest(self, request):
        """
        put request into queue tail
        """
##        begin = datetime.datetime.now()
##        if (request.type == 0) or(request.type == 1):
##            ##message
##            msg = request.message
##            self.info("<BaseService>debug:try put message msg type %d, id %d, session[%08X]..."%(
##                msg.type, msg.id, msg.session))
        with self.__request_lock:
            length = len(self.__request_list)
            if length >= self.__max_request:
                self.console("<BaseService> put request fail, request queue is full")
                self.error("<BaseService> put request fail, request queue is full")
                return False
            self.__request_list.append(request)
            self.__request_available.set()
                
##            diff = datetime.datetime.now() - begin
##            elapse_seconds = diff.seconds + float(diff.microseconds)/1000000
##            if (request.type == 0) or(request.type == 1):
##                ##message
##                msg = request.message
##                self.info("<BaseService>debug:put message in %.1f second(s), msg type %d, id %d, session[%08X]"%(
##                    elapse_seconds, msg.type, msg.id, msg.session))
##            else:
##                ##
##                self.info("<BaseService>debug:put request in %.1f second(s), request type %d, session[%08X]"%(
##                    elapse_seconds, request.type, request.session_id))
            return True

    def putRequestList(self, request_list):
        with self.__request_lock:
            length = len(self.__request_list)
            if length >= self.__max_request:
                self.console("<BaseService> put request list fail, request queue is full")
                self.error("<BaseService> put request list fail, request queue is full")
                return False
            self.__request_list.extend(request_list)
            self.__request_available.set()
            return True
        
    
    def insertRequest(self, request):
        """
        put request into queue head
        """
##        begin = datetime.datetime.now()
        with self.__request_lock:
            length = len(self.__request_list)
            if length >= self.__max_request:
                self.console("<BaseService> insert request fail, request queue is full")
                self.error("<BaseService> insert request fail, request queue is full")
                return False
            self.__request_list.insert(0, request)
            self.__request_available.set()
##            diff = datetime.datetime.now() - begin
##            elapse_seconds = diff.seconds + float(diff.microseconds)/1000000
##            if (request.type == 0) or(request.type == 1):
##                ##message
##                msg = request.message
##                self.info("<BaseService>debug:insert message in %.1f second(s), msg type %d, id %d, session[%08X]"%(
##                    elapse_seconds, msg.type, msg.id, msg.session))
##            else:
##                ##
##                self.info("<BaseService>debug:insert request in %.1f second(s), request type %d, session[%08X]"%(
##                    elapse_seconds, request.type, request.session_id))
            return True
        
    """
    method need override by subclass
    """

    """
    onStart
    @return:
    False = initial fail, stop service
    True = initial success, start main service
    """
    def onStart(self):
        pass

    def onStop(self):
        pass

    def OnRequestReceived(self, request):
        pass

