# encoding: utf8
import threading



class ResetEvent():

    def __init__(self):
        self.__cond = threading.Condition(threading.RLock())
        self.__flag = False

    def isSet(self):
        return self.__flag

    is_set = isSet

    def set(self):
        self.__cond.acquire()
        try:
            self.__flag = True
            self.__cond.notify()
        finally:
            self.__cond.release()

    def clear(self):
        self.__cond.acquire()
        try:
            self.__flag = False
        finally:
            self.__cond.release()

    def wait(self, timeout=None):
        self.__cond.acquire()
        try:
            if not self.__flag:
                self.__cond.wait(timeout)
            if self.__flag==True:
                self.__flag = False
            return self.__flag
        finally:
            self.__cond.release()
