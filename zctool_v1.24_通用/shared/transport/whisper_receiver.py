#!/usr/bin/python
import io
import os
import os.path
import datetime
import logging
from whisper_strip import *

class WhisperReceiver(object):
    max_timeout = 100
    def __init__(self, filename,
                 file_size, block_size, strip_length):
        self.filename = filename
        self.file_size = file_size
        self.block_size = block_size
        self.strip_length = strip_length 
        ##key = strip id, value = list of true/false
        self.receiving_strip = {}
        self.counter = 0
        self.received = 0
        self.strip_size = 0
        ##speed
        self.last_received = 0
        self.last_time = datetime.datetime.now()
        ##strip id
        self.appending_strip = set()
        
    def prepare(self):
        """
        create&allocate file/strip/block
        """
        if os.path.exists(self.filename):
            os.remove(self.filename)
        buffer_size = self.block_size * self.strip_length
        file_object = io.FileIO(self.filename, "w+")
        self.writer = io.BufferedRandom(file_object, buffer_size)
        
        ##slice strip
        self.strip_size = self.block_size * self.strip_length
        remainder = self.file_size%self.strip_size
        if 0 == remainder:
            total_strip = self.file_size/self.strip_size
        else:
            total_strip = ((self.file_size - remainder) / self.strip_size) + 1
            
        for strip_id in range(total_strip):
            self.appending_strip.add(strip_id)            
        return True
    
    def writeData(self, strip_id, block_id, data):
        if self.writer.closed:
            return True
        if strip_id not in self.appending_strip:
            ##already finished
            return True
        if not self.receiving_strip.has_key(strip_id):
            ##new strip
            strip = WhisperStrip(strip_id, self.file_size, self.block_size, self.strip_length)
            self.receiving_strip[strip_id] = strip
        strip = self.receiving_strip[strip_id]
        self.counter = 0
        if not strip.writeBlock(block_id, data):
##            logging.info("<Whisper>debug:write block fail, block %d.%d"%(
##                strip_id, block_id))
            return False
        
        if not strip.isFinished():
            return True
        
        ##finished
        potision = strip.getPosition()
        strip_data = strip.getData()
        data_length = len(strip_data)
        self.writer.seek(potision)
        self.writer.write(strip_data)
        self.received += data_length
        
        del self.receiving_strip[strip_id]
        
        self.appending_strip.remove(strip_id)
        
        if 0 == len(self.appending_strip):
##            logging.info("<Whisper>debug:write finish, %d / %d bytes, %d / %d strip"%(
##                self.received, self.file_size,
##                self.finish_strip, self.total_strip))                
            self.writer.close()
        return True            
    
    def isFinished(self):
        return (0 == len(self.appending_strip))

    def check(self):
        """
        @return:True=timeout
        """
        self.counter += 1
        if self.counter > self.max_timeout:
            return False
        else:
            return True

    def statistic(self):
        """
        @return:current, total, percentage, speed
        """
        timestamp = datetime.datetime.now()
        processed = self.received - self.last_received
        percentage = float(self.received)*100/self.file_size
        if processed <= 0:
            return self.received, self.file_size, percentage, 0
        diff = timestamp - self.last_time
        elapse_seconds = diff.seconds + float(diff.microseconds)/1000000
        if elapse_seconds <= 0:
            return self.received, self.file_size, percentage, 0
        speed = float(processed)/elapse_seconds##bps
        self.last_received = self.received
        self.last_time = timestamp
        return self.received, self.file_size, percentage, speed
