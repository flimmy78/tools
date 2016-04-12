#!/usr/bin/python
import threading
from state_define import *

class BaseSession(object):

    def __init__(self, session_id):
        self.session_id = 0
        self.task_type = 0
        self.initialed = False
        self.current_state = 0
        self.initial_message = None
        self.request_module = ""
        self.request_session = 0
        self.timer_id = 0
        self.session_id = session_id
        self.blocked = False
        self.lock = threading.RLock()
        ##cached message,FIFO
        self.message = []
        self.reset()

    def reset(self):
        """
        reset session params,should override
        """
        with self.lock:
            self.task_type = 0
            self.initialed = False
            self.current_state = 0
            self.request_module = ""
            self.request_session = 0
            self.timer_id = 0
            self.initial_message = None
            self.state_specified = False
            self.blocked = False
            self.message = []

    def occupy(self, task_type):
        with self.lock:
            self.task_type = task_type
            return True

    def isInitialed(self):
        with self.lock:
            return self.initialed
    
    def initial(self, msg):
        """
        initial session message,should override
        """
        with self.lock:
            self.initial_message = msg
            self.current_state = state_initial
            self.request_session = msg.session
            self.request_module = msg.sender
            self.initialed = True

    def isFinished(self):
        with self.lock:
            return (state_finish == self.current_state)

    def finish(self):
        with self.lock:
            self.current_state = state_finish

    def setState(self, new_state):
        with self.lock:
            self.current_state = new_state
            self.state_specified = True

    def putMessage(self, message):
        with self.lock:
            self.message.append(message)

    def insertMessage(self, message):
        with self.lock:
            self.message.insert(0, message)

        
    def fetchMessage(self):
        """
        get all & clear
        """
        with self.lock:
            result = self.message
            self.message = []
            return result
        

