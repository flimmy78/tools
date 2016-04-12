#!/usr/bin/python
import threading
from send_task import *
from service.performance_test import *

class SendTaskManager(object):
    def __init__(self, max_capacity = 1024, max_timeout = 5, max_retry = 3):
        self.min_id = 1
        self.max_id = self.min_id + max_capacity
        self.max_capacity = max_capacity
        self.max_timeout = max_timeout
        self.max_retry = max_retry
        
        self.task_map = {}
        self.timeout = {}
        self.retry = {}
        self.allocated = {}
        
        self.lock = threading.RLock()
        for task_id in range(self.min_id, self.max_id):
            task = SendTask(task_id)
            self.task_map[task_id] = task
            self.timeout[task_id] = 0
            self.retry[task_id] = 0
            self.allocated[task_id] = False
            
        self.last_id = 0
        
    def allocate(self, request):
        with self.lock:                
            result = []
            count = 0
            for offset in range(self.max_capacity):
                task_id = (self.last_id + 1 + offset)%self.max_capacity + self.min_id
                if not self.allocated[task_id]:
                    result.append(task_id)
                    self.allocated[task_id] = True
                    self.timeout[task_id] = 0
                    self.retry[task_id] = 0
                    count += 1
                    if count >= request:
                        break;
            if count < request:
                ##release
                for task_id in result:
                    self.allocated[task_id] = False
                return []
            return result

    def deallocate(self, task_list):
        with self.lock:
            result = []
            for task_id in task_list:
                if (task_id < self.min_id) or (task_id > self.max_id):
                    continue
                if self.allocated[task_id]:
                    self.allocated[task_id] = False
                    self.timeout[task_id] = 0
                    self.retry[task_id] = 0
    
        
    def checkTimeout(self):
        with self.lock:
            timeout_task = []
            deallocate_task = []                
            for task_id in self.allocated.keys():
                if self.allocated[task_id]:
                    self.timeout[task_id] += 1
                    if self.timeout[task_id] >= self.max_timeout:                        
                        self.timeout[task_id] = 0
                        self.retry[task_id] += 1
                        if self.retry[task_id] > self.max_retry:
                            ##need remove
                            deallocate_task.append(task_id)
                        else:
                            ##need retry
                            timeout_task.append(task_id)
            return timeout_task, deallocate_task

    def update(self, id_list, send_list):
        """
        send_list:list of (packet, ip, port)
        """
        with self.lock:
            updated = 0
            for i in range(len(id_list)):
                task_id = id_list[i]
                if (task_id < self.min_id) or (task_id > self.max_id):
                    continue                
                if self.allocated[task_id]:
                    packet = send_list[i][0]
                    remote_ip = send_list[i][1]
                    remote_port = send_list[i][2]
                    self.task_map[task_id].initial(packet, remote_ip, remote_port)
                    updated += 1
            return updated

    def fetch(self, id_list):
        """
        return:list of (packet, ip, port)
        """
        with self.lock:
            result = []
            for task_id in id_list:
                if self.allocated[task_id]:
                    task = self.task_map[task_id]
                    result.append((task.getData(), task.getIP(), task.getPort()))

            return result

if __name__ == '__main__':
    import time
##    import logging
    from service.loop_thread import *
    
##    handler = logging.StreamHandler(sys.stdout)
##    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
##    handler.setFormatter(formatter)
##    handler.setLevel(logging.DEBUG)
##    root = logging.getLogger()
##    root.addHandler(handler)
##    root.setLevel(logging.DEBUG)

    interval = 1
    count = 5000
    batch = 50
    repeat = count/batch
    max_channel = 5
    duration = 20
    
    manager = SendTaskManager(count * max_channel * interval * 2)
    

    class Proxy(LoopThread):
        def __init__(self):
            LoggerHelper.__init__(self, "proxy")
            LoopThread.__init__(self, interval)
            self.success = 0
            self.fail = 0
            
        def onLoop(self):
            id_list = []
            for i in range(repeat):
                result = manager.allocate(batch)
                if 0 != len(result):
                    id_list.extend(result)
                    self.success += len(result)
                else:
                    self.fail += batch

            manager.deallocate(id_list)
           

    print "test start"
    channels = []   
    for i in range(max_channel):
        channels.append(Proxy())
        
    with TestUnit("batch test"):
        for channel in channels:
            channel.start()
            
        for i in range(duration):
            manager.checkTimeout()            
            time.sleep(1)
            
        success = 0
        fail = 0        
        for channel in channels:
            channel.stop()
            success += channel.success
            fail += channel.fail

    print "success %d, fail %d"%(success, fail)
    result = PerfomanceManager.get().statistic()
    for entry in result:
        print entry.name, entry.count, entry.average, entry.max, entry.min, entry.total
    print "test finish"
    
        
