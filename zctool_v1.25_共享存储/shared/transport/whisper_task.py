#!/usr/bin/python
import threading

class TaskTypeEnum(object):
    write = 0
    read = 1
    
class WhisperTask(object):
    def __init__(self, task_id, task_type, proxy):
        self.task_id = task_id
        self.task_type = task_type
        self.proxy = proxy
        self.lock = threading.RLock()
        self.reset()
        
    def reset(self):
        with self.lock:
            self.file_id = ""
            self.filename = ""
            self.is_server = False
            self.finished = False
            self.success = False
            self.window_size = 1
            ##congestion control
            self.ack_counter = 0
            ##decreate trigger
            self.max_lost = 3
            self.window_threhold = 128
            self.control_step = 1
            self.processed = 0
            self.total = 0
            ##0~100
            self.progress = 0
            ##Bps
            self.speed = 0
            self.file_size = 0
            self.block_size = 0
            self.strip_length = 0
            self.remote_ip = ""
            self.remote_port = 0
            self.remote_data_port = []
            self.remote_data_port_count = 0
            self.remote_task = 0
            self.remote_file = ""
            self.sender = None
            self.receiver = None
            self.counter = 0
            self.check_counter = 0
                 
        
    def allocate(self, file_id, filename, is_server):
        with self.lock:
            self.file_id = file_id
            self.filename = filename        
            self.is_server = is_server

    def getTaskID(self):
        return self.task_id

    def getTaskType(self):
        return self.task_type

    def getFileID(self):
        return self.file_id

    def isFinished(self):
        return self.finished

    def isSuccess(self):
        return self.success

    def getProcessed(self):
        return self.processed

    def getTotal(self):
        return self.total

    def getProgress(self):
        return self.progress

    def getSpeed(self):
        return self.speed

    def setWindowSize(self, window_size):
        with self.lock:
            self.window_size = window_size

    def getWindowSize(self):
        return self.window_size

    def onDataAck(self):
        with self.lock:
            ##congest control
            self.ack_counter += 1
            if self.ack_counter >= self.getWindowSize():
                self.increaseWindow()

    def onDataLost(self, count):        
        if count >= self.max_lost:
            self.decreaseWindow()

    def increaseWindow(self):
        with self.lock:
            current = self.getWindowSize()
            if current < self.window_threhold:
                new_window = current * 2
                if new_window > self.window_threhold:
                    new_window = self.window_threhold
            else:
                new_window = current + self.control_step
    ##        logging.info("<Whisper>debug:increase window to %d / %d"%(
    ##            new_window, self.window_threhold))
            self.setWindowSize(new_window)
            self.ack_counter = 0

    def decreaseWindow(self):
        with self.lock:
            current = self.getWindowSize()
            self.window_threhold = current
            new_window = current - current/3
    ##        logging.info("<Whisper>debug:decrease window to %d / %d"%(
    ##            new_window, self.window_threhold))
            self.setWindowSize(new_window)
            self.ack_counter = 0        

    def sendCommand(self, command, remote_ip, remote_port):
        return self.proxy.sendCommand(command, remote_ip, remote_port)

    def sendData(self, request_list):
        """
        @request_list:list of (data msg, remote_ip, remote_port)
        """
        return self.proxy.sendData(request_list)

##    def onStart(self):
##        self.proxy.onTaskStart(self.task_id, self.task_type)
##
##    def onProgress(self, current, total, percent, speed):
##        self.proxy.onTaskProgress(self.task_id, self.task_type,
##                                  current, total, percent, speed)
##
##    def onSuccess(self, file_id):
##        self.proxy.onTaskSuccess(self.task_id, self.task_type,
##                                 file_id)
##
##    def onFail(self):
##        self.proxy.onTaskFail(self.task_id, self.task_type)

    def isWriteTask(self):
        return (TaskTypeEnum.write == self.task_type)

    def isReadTask(self):
        return (TaskTypeEnum.read == self.task_type)

    def isServer(self):
        return self.is_server

    def handleData(self, command, sender_ip, sender_port):
        pass
    
    def handleDataAck(self, command, sender_ip, sender_port):
        pass
    
    def handleFinish(self, command, sender_ip, sender_port):
        pass
    
    def handleFinishAck(self, command, sender_ip, sender_port):
        pass

    def check(self):
        pass
