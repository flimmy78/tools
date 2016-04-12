#!/usr/bin/python
import threading
import logging
import datetime
from message_define import *
from timed_invoker import *

class TimerService(object):
    """
    usage:
    isRunning():
    start():
    stop():
    setTimer(timeout, receive_session):
        invoke timeout event to [receive_session] after [timeout] seconds
        @return:timer_id
        
    setLoopTimer(timeout, receive_session):
        continues invoke timeout event to [receive_session] after [timeout] seconds
        @return:timer_id
        stop by clearTimer()
        
    setTimedEvent(event, timeout):
        invoke specified [event] to handler after [timeout] seconds
        @return:timer_id
        
    setLoopTimedEvent(event, timeout):
        continues invoke specified [event] to handler after [timeout] seconds
        @return:timer_id
        stop by clearTimer()
        
    clearTimer(timer_id):
        cancel timeout count down

    bindEventHandler(handler):
        handler must has callable by self.handler(event)
        
    override methods
    onStart():return False to cancel start process
    onStop():
    onLoop():customize loop process here

    created akumas 2013.8.8
    """
    class TimeCounter(object):
        timer_id = 0
        receive_session = 0
        timeout = 0
        count_down = 0
        is_loop = False
        specify_event = None

    event_handler = None
    max_timer = 1000
    def __init__(self, logger_name, interval = 1):
        self.logger = logging.getLogger(logger_name)
        self.invoker = TimedInvoker(self.onLoop,
                                    interval)
        self.timer_map = {}
        self.lock = threading.RLock()
        self.seed = 0

    def start(self):
        self.invoker.start()
        return True

    def stop(self):
        self.invoker.stop()
        return True
        
    def setTimer(self, timeout, receive_session):
        """
        invoke timeout event to [receive_session] after [timeout] seconds
        @return:timer_id
        """
        with self.lock:
            timer = TimerService.TimeCounter()
            seed = self.seed
            for i in range(TimerService.max_timer):
                timer_id = (seed + i)%TimerService.max_timer + 1
                if not self.timer_map.has_key(timer_id):
                    ##available
                    self.seed = (seed + i)%TimerService.max_timer            
                    timer.timer_id = timer_id
                    timer.receive_session = receive_session
                    timer.timeout = timeout
                    timer.count_down = timeout
                    self.timer_map[timer_id] = timer
##                    self.logger.info("<TimerService>debug:timer created, timeout %d, session [%08X], id %d"%(
##                        timeout, receive_session, timer.timer_id))
                    return timer.timer_id
            else:
##                self.logger.error("<TimerService>set timer fail, no more timer available")
                return -1
        
    def setLoopTimer(self, timeout, receive_session):
        """
        continues invoke timeout event to [receive_session] after [timeout] seconds
        @return:timer_id
        stop by clearTimer()
        """
        with self.lock:
            timer = TimerService.TimeCounter()
            seed = self.seed
            for i in range(TimerService.max_timer):
                timer_id = (seed + i)%TimerService.max_timer + 1
                if not self.timer_map.has_key(timer_id):
                    ##available
                    self.seed = (seed + i)%TimerService.max_timer            
                    timer.timer_id = timer_id
                    timer.receive_session = receive_session
                    timer.timeout = timeout
                    timer.count_down = timeout
                    timer.is_loop = True
                    self.timer_map[timer_id] = timer
##                    self.logger.info("<TimerService>debug:loop timer created, timeout %d, session [%08X], id %d"%(
##                        timeout, receive_session, timer.timer_id))
                    return timer.timer_id
            else:
##                self.logger.error("<TimerService>set loop timer fail, no more timer available")
                return -1        
        
    def setTimedEvent(self, event, timeout):
        """
        invoke specified [event] to handler after [timeout] seconds
        @return:timer_id
        """
        with self.lock:
            timer = TimerService.TimeCounter()
            seed = self.seed
            for i in range(TimerService.max_timer):
                timer_id = (seed + i)%TimerService.max_timer + 1
                if not self.timer_map.has_key(timer_id):
                    ##available
                    self.seed = (seed + i)%TimerService.max_timer            
                    timer.timer_id = timer_id
                    ##determined by event
                    timer.receive_session = 0
                    timer.timeout = timeout
                    timer.count_down = timeout
                    timer.specify_event = event
                    self.timer_map[timer_id] = timer
##                    self.logger.info("<TimerService>debug:timed event created, timeout %d, id %d"%(
##                        timeout, timer.timer_id))
                    return timer.timer_id
            else:
##                self.logger.error("<TimerService>set timed event fail, no more timer available")
                return -1
        
    def setLoopTimedEvent(self, event, timeout):
        """
        continues invoke specified [event] to handler after [timeout] seconds
        @return:timer_id
        stop by clearTimer()
        """
        with self.lock:
            timer = TimerService.TimeCounter()
            seed = self.seed
            for i in range(TimerService.max_timer):
                timer_id = (seed + i)%TimerService.max_timer + 1
                if not self.timer_map.has_key(timer_id):
                    ##available
                    self.seed = (seed + i)%TimerService.max_timer            
                    timer.timer_id = timer_id
                    ##determined by event
                    timer.receive_session = 0
                    timer.timeout = timeout
                    timer.count_down = timeout
                    timer.specify_event = event
                    timer.is_loop = True
                    self.timer_map[timer_id] = timer
##                    self.logger.info("<TimerService>debug:loop timed event created, timeout %d, id %d"%(
##                        timeout, timer.timer_id))
                    return timer.timer_id
            else:
##                self.logger.error("<TimerService>set loop timed event fail, no more timer available")
                return -1
        
    def clearTimer(self, timer_id):
        """
        cancel timeout count down
        """
        with self.lock:
            if self.timer_map.has_key(timer_id):
                del self.timer_map[timer_id]
##                self.logger.info("<TimerService>debug:timer %d removed"%timer_id)

    def bindEventHandler(self, handler):
        """
        handler must has callable by self.handler(event)
        """
        self.event_handler = handler        

    def onLoop(self):
        """
        customize loop process here
        """
        with self.lock:
##            self.logger.info("<TimerService>debug:onLoop invoked")
            
            event_list = []
            clear_list = []
            for timer in self.timer_map.values():
                timer.count_down -= 1
                if 0 == timer.count_down:
                    ##timeout   
                    if self.event_handler:
                        if not timer.specify_event:
                            event = getEvent(EventDefine.timeout)
                            event.session = timer.receive_session
                            event.sequence = timer.timer_id
                        else:
                            event = timer.specify_event
                            
##                        self.logger.info("<TimerService>debug:timer %d invoked, session[%08X]"%(
##                            timer.timer_id, timer.receive_session))
                        event_list.append(event)
                        
                        
                    if timer.is_loop:
                        ##loop timer
                        timer.count_down = timer.timeout                       
                    else:
                        ##clear
                        clear_list.append(timer.timer_id)
            ##end for timer in self.timer_map.values():
            if 0 != len(clear_list):
                for timer_id in clear_list:                        
                    del self.timer_map[timer_id]
                    
        if 0 != len(event_list):
            ##batch invoked
            self.event_handler(event_list)
                
if __name__ == '__main__':
    class Handler(object):
        def onTimeoutEvent(self, event_list):
            for event in event_list:
                print "on timeout, session =", event.session

    handler = Handler()
    timer = TimerService("timer")
    timer.bindEventHandler(handler.onTimeoutEvent)
    timer.start()
    id1 = timer.setTimer(2, 1)
    id2 = timer.setLoopTimer(5, 2)
    id3 = timer.setTimer(10, 3)
    id4 = timer.setLoopTimer(4, 4)
    print id1,id2,id3,id4
    
    import time
    time.sleep(10)
    timer.clearTimer(id4)
    
    time.sleep(20)
    timer.stop()
    
