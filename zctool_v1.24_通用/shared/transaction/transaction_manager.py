#!/usr/bin/python
import threading
import logging
from service.service_status import *
from service.message_define import *
from base_session import *
from service.reset_event import ResetEvent

class TransactionManager(object):
    
    min_session_id = 1
    max_session_id = 1
    wait_interval = 1
    invoke_interval = 0.02      ##20ms
    check_interval = 0.05       ##50ms
    
    def __init__(self, logger_name, min_id = 1, session_count = 1000, work_thread = 1):
        self.logger = logging.getLogger(logger_name)
        self.lock = threading.RLock()
        
        self.status_lock = threading.RLock()
        self.status = StatusEnum.stopped
        self.thread_index = 0
        
        self.task_lock = []
        self.task_queue = []
        self.task_available = []
        
        ##key = task type, value = task
        self.task_map = {}
        ##key = session id, value = session
        self.session_map = {}
        ##key = session id, value = allocated
        self.allocate_map = {}
        self.min_session_id = min_id
        self.max_session_id = min_id + session_count - 1
        self.session_count = session_count
        self.last_session = min_id - 1
        for session_id in range(self.min_session_id, self.max_session_id + 1):
            session = self.createSession(session_id)
            self.session_map[session_id] = session
            self.allocate_map[session_id] = False
            
        self.logger.info("<TaskManager>transaction session created, id %d ~ %d"%(
            self.min_session_id, self.max_session_id))

        self.invoke_thread = []
        self.thread_count = work_thread
        for i in range(work_thread):
            self.invoke_thread.append(threading.Thread(target=self.invokeProcess))
            self.task_lock.append(threading.RLock())
            self.task_available.append(ResetEvent())   #self.task_available.append(threading.Event())
            self.task_queue.append([])
            
        self.logger.info("<TaskManager>%d work thread(s), 1 check thread(s) ready"%(
            work_thread))
        
    def addTask(self, task_type, task):
        with self.lock:
            if self.task_map.has_key(task_type):
                self.warn("<TaskManager>add task fail, type %d already exists"%task_type)
                return False
            self.task_map[task_type] = task
            self.logger.info("<TaskManager>add task success, type %d" % task_type)
            return True

    def createSession(self, session_id):
        """
        create session instance, override by inherited class if necessary
        """
        session = BaseSession(session_id)
        return session

    def allocTransaction(self, task_type):
        with self.lock:
            current_offset = self.last_session + 1 - self.min_session_id
            for offset in range(self.session_count):
                session_id = self.min_session_id + (current_offset + offset)%self.session_count
                if self.allocate_map.has_key(session_id):
                    if not self.allocate_map[session_id]:
                        ##unallocated
                        session = self.session_map[session_id]
                        self.last_session = session_id
                        session.occupy(task_type)
                        self.allocate_map[session_id] = True
                        return session_id
            return None
                
    def deallocTransaction(self, session_id):
        if (session_id < self.min_session_id) or (session_id > self.max_session_id):
            return False
        with self.lock:
            if self.allocate_map[session_id]:
                ##allocated
                self.allocate_map[session_id] = False
                self.session_map[session_id].reset()
                    
    def terminateTransaction(self, session_id):
        if (session_id < self.min_session_id) or (session_id > self.max_session_id):
            return
        with self.lock:
            if self.allocate_map[session_id]:
                ##allocated
                msg = getEvent(EventDefine.terminate)
                msg.session = session_id
                session = self.session_map[session_id]
                session.insertMessage(msg)
                self.invokeTransaction(session_id)
        
    def invokeTransaction(self, session_id):
        thread_index = session_id % self.thread_count
##        self.logger.info("<TaskManager>debug:invoke session [%08X] to T%d"%(
##            session_id, thread_index))

        with self.task_lock[thread_index]:
            self.task_queue[thread_index].append(session_id)
            self.task_available[thread_index].set()
            
    def startTransaction(self, session_id, msg):
        return self.appendMessage(session_id, msg)

    def processMessage(self, session_id, msg):
        return self.appendMessage(session_id, msg)

    def containsTransaction(self, session_id):
        """
        if processing transaction allocated
        """
        if (session_id < self.min_session_id) or (session_id > self.max_session_id):
            return False
        with self.lock:
            return self.allocate_map[session_id]
        
    def appendMessage(self, session_id, msg):
        with self.lock:
            if not self.containsTransaction(session_id):
                self.logger.warn("<TaskManager>append message to session fail, invalid task session [%08X]"%(
                    session_id))
                return False
        session = self.session_map[session_id]
        session.putMessage(msg)
        self.invokeTransaction(session_id)
        return True

    def start(self):
        with self.status_lock:
            if StatusEnum.stopped != self.status:
                return False
            self.status = StatusEnum.running   
            for i in range(self.thread_count):
                self.invoke_thread[i].start()
            self.logger.info("<TaskManager>service started")
            return True

    def stop(self):
        with self.status_lock:
            if StatusEnum.stopped == self.status:
                return
            if StatusEnum.running == self.status:
                self.status = StatusEnum.stopping

                for i in range(self.thread_count):
                    self.task_available[i].set()

        for i in range(self.thread_count):
            self.invoke_thread[i].join()
        with self.status_lock:
            self.status = StatusEnum.stopped
        self.logger.info("<TaskManager>service stopped")

    
    def invokeProcess(self):
        with self.status_lock:            
            index = self.thread_index
            self.thread_index += 1
        
##        self.logger.info("<TaskManager>debug:work thread T%d started"%(index))
        while StatusEnum.running == self.status:
            
            ##wait for signal
            self.task_available[index].wait(self.wait_interval)
            
            if StatusEnum.running != self.status:
                ##double protect
                break      
            
            ##check task
            with self.task_lock[index]:
                if 0 == len(self.task_queue[index]):
                    continue
                request_list = self.task_queue[index]
                self.task_queue[index] = []                
                
            with self.lock:
                ##process session message
                session_list = []
                for session_id in request_list:
                    
                    if (session_id < self.min_session_id) or (session_id > self.max_session_id):
                        self.logger.warn("<TaskManager>invoke session fail, invalid session [%08X]"%(session_id))
                        continue
                    
                    if session_id in session_list:
                        continue
                    
                    if not self.allocate_map[session_id]:
                        self.logger.warn("<TaskManager>invoke session fail, session [%08X] not allocated"%(session_id))
                        continue
                    
                    session_list.append(session_id)                    
                
            ##unlock
            for session_id in session_list:
                session = self.session_map[session_id]                
                task_type = session.task_type
                if not self.task_map.has_key(task_type):
                    self.logger.warn("<TaskManager>invoke session fail, invalid task %d for session [%08X]"%(
                                                                                                             task_type, session_id))
                    self.deallocTransaction(session_id)
                    continue
                task = self.task_map[task_type]
                message_list = session.fetchMessage()
                for msg in message_list:
                    try:
                        if not session.isInitialed():
                            task.initialSession(msg, session)
                            
##self.logger.info("<TaskManager>debug:session[%08X] initialed by T%d"%(
##                            	session_id, index))
                            task.invokeSession(session)
                        else:
                            task.processMessage(msg, session)
                            
##self.logger.info("<TaskManager>debug:session[%08X] message processed by T%d"%(
##                            	session_id, index))
                        if session.isFinished():
                            self.deallocTransaction(session_id)
                            break
                    except Exception as e:
                        self.logger.exception("<TaskManager>process messge exception in thread %d, session[%08X], msg %d, exception:%s"%(
                                                                                                                                         index, session_id, msg.id, e.args[0]))
                        self.deallocTransaction(session_id)
                        break
                    
##        self.logger.info("<TaskManager>debug:work thread T%d stopped"%(index))
        
        
