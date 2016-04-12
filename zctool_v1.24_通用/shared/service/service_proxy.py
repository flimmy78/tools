#!/usr/bin/python
import sys
import io
import logging
import logging.handlers
import os
import os.path
import uuid
import shutil
from ConfigParser import *
from service.message_define import *

class ServiceProxy(object):
    
    root_path = "/var/zhicloud"
    
    def __init__(self, service_type, log_level = logging.INFO):
        self.type = service_type
        if NodeTypeDefine.data_server == service_type:
            self.type_name = "data_server"
        elif NodeTypeDefine.control_server == service_type:
            self.type_name = "control_server"
        elif NodeTypeDefine.node_client == service_type:
            self.type_name = "node_client"
        elif NodeTypeDefine.storage_server == service_type:
            self.type_name = "storage_server"
        elif NodeTypeDefine.statistic_server == service_type:
            self.type_name = "statistic_server"
        elif NodeTypeDefine.manage_terminal == service_type:
            self.type_name = "manage_terminal"
        elif NodeTypeDefine.http_gateway == service_type:
            self.type_name = "http_gateway"
        elif NodeTypeDefine.data_index == service_type:
            self.type_name = "data_index"
        elif NodeTypeDefine.data_node == service_type:
            self.type_name = "data_node"
        elif NodeTypeDefine.storage_manager == service_type:
            self.type_name = "storage_manager"
        elif NodeTypeDefine.storage_client == service_type:
            self.type_name = "storage_client"
        elif NodeTypeDefine.storage_portal == service_type:
            self.type_name = "storage_portal"
        elif NodeTypeDefine.storage_object == service_type:
            self.type_name = "storage_object"
        elif NodeTypeDefine.intelligent_router == service_type:
            self.type_name = "intelligent_router"

        self.log_path = os.path.join(self.root_path, "log")
        self.running_path = os.path.join(self.root_path, "running")
        self.tmp_path = os.path.join(self.root_path, "tmp")
        self.config_path = os.path.join(self.root_path, "config")
        self.module_path = os.path.join(self.config_path, self.type_name)                
            
        self.log_level = log_level
        self.pidfile = ""
        self.log_file = ""
        self.out_file = ""
        
        self.config_file = os.path.join(self.module_path, "node.conf")
        self.domain = ""
        self.node = ""
        self.ip = ""
        self.group_ip = ""
        self.group_port = 0

        self.server_info = os.path.join(self.config_path, "server.info")
        self.server = ""
        self.rack = ""
        self.server_name = ""
        
        self.service = None
        self.config_loaded = False

        ##make path /var/zhicloud
        if not os.path.exists(self.root_path):
            os.mkdir(self.root_path)
        ##/var/zhicloud/log
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)
        ##/var/zhicloud/running
        if not os.path.exists(self.running_path):
            os.mkdir(self.running_path)
        ##/var/zhicloud/tmp
        if not os.path.exists(self.tmp_path):
            os.mkdir(self.tmp_path)
        ##/var/zhicloud/config
        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)
            ##check server info
            old_server_info = "/home/zhicloud/server.info"
            ##copy to new location
            content = io.open(old_server_info, "rb").read()
            new_info = io.open(self.server_info, "wb")
            new_info.write(content)
            new_info.close()
            self.console("<ServiceProxy>copy server info '%s' to '%s'"%(
                        old_server_info, self.server_info))
            
        ##/var/zhicloud/config/type_name
        if not os.path.exists(self.module_path):
            os.mkdir(self.module_path)
            ##copy node conf
            old_node_conf = "/home/zhicloud/%s/node.conf"%(self.type_name)
            if os.path.exists(old_node_conf):
                ##copy to new location
                content = io.open(old_node_conf, "rb").read()
                new_node_conf = os.path.join(self.module_path, "node.conf")
                
                new_info = io.open(new_node_conf, "wb")
                new_info.write(content)
                new_info.close()
                self.console("<ServiceProxy>copy node conf '%s' to '%s'"%(
                            old_node_conf, new_node_conf))
                
            ##move old config
            old_config = os.path.join("/home/zhicloud", self.type_name)
            name_list = os.listdir(old_config)
            for path_name in name_list:
                source_path = os.path.join(old_config, path_name)
                if os.path.isdir(source_path):
                    ##move to new dest
                    target_path = os.path.join(self.module_path, path_name)
                    self.console("<ServiceProxy>begin copy config path '%s' to '%s'..."%(
                        source_path, target_path))
                    shutil.copytree(source_path, target_path)
                    self.console("<ServiceProxy>config path '%s' moved to '%s'"%(
                        source_path, target_path))

    def attachLogger(self):
        if 0 != len(self.log_file):
            path = os.path.dirname(self.log_file)
            if not os.path.exists(path):
                ##make path
                os.makedirs(path)
                self.console("<ServiceProxy>log path created, path '%s'"%(path))
            ##save for 5 days
            handler = logging.handlers.TimedRotatingFileHandler(
                self.log_file, when='D', backupCount=30, encoding="utf-8")
            
            formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ##        formatter = logging.Formatter("%(asctime)s [%(levelname)s] <%(name)s> %(message)s")
            handler.setFormatter(formatter)
            handler.setLevel(self.log_level)
            root = logging.getLogger()
            root.addHandler(handler)
            root.setLevel(self.log_level)
            self.console("<ServiceProxy>log write to '%s'"%(self.log_file))
            
    def redirectOutput(self):
        ##close stdint/stdout
        with io.open(os.devnull, "r") as pipe:
            os.dup2(pipe.fileno(), sys.stdin.fileno())
            self.console("<ServiceProxy>stdin closed")
            
        if 0 != len(self.out_file):
            path = os.path.dirname(self.out_file)
            if not os.path.exists(path):
                ##make path
                os.makedirs(path)
                self.console("<ServiceProxy>output path created, path '%s'"%(path))
                
            with io.open(self.out_file, "wb") as pipe:
                self.console("<ServiceProxy>stdout/stderr redirect to '%s'"%(self.out_file))
                os.dup2(pipe.fileno(), sys.stdout.fileno())
                os.dup2(pipe.fileno(), sys.stderr.fileno())            

    def loadConfig(self):
        ##communication
        parser = ConfigParser()        
        
        if not os.path.exists(self.config_file):
            
            ##defaul values
            self.domain     = DefaultValues.domain
            self.group_ip   = DefaultValues.multicast_ip
            self.group_port = DefaultValues.multicast_port
            
            if NodeTypeDefine.data_server != self.type:
                ##mac or random mac
                mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
                ##format:"%default"_"%mac string"
                self.node = "%s_%s"%(self.type_name, mac_string)
            else:
                ##fix "data_server" for ds
                self.node = "%s"%(self.type_name)
            
            ##create default config
            parser.set("DEFAULT", "domain",     self.domain)
            parser.set("DEFAULT", "node",       self.node)
            parser.set("DEFAULT", "ip",         "")
            parser.set("DEFAULT", "group_ip",   self.group_ip)
            parser.set("DEFAULT", "group_port", self.group_port)
            
            with io.open(self.config_file, "wb") as config:
                ##write & truncate & binary
                parser.write(config)            
            
        else:
            parser.read(self.config_file)
            self.domain     = parser.get("DEFAULT",    "domain").strip()
            self.node       = parser.get("DEFAULT",    "node").strip()
            self.ip         = parser.get("DEFAULT",    "ip").strip()
            self.group_ip   = parser.get("DEFAULT",    "group_ip").strip()
            self.group_port = parser.getint("DEFAULT", "group_port")

        ##physical location
        if NodeTypeDefine.manage_terminal != self.type:
            parser = ConfigParser()        
            if not os.path.exists(self.server_info):
                
                ##defaul values
                
                ##server:uuid
                self.server = uuid.UUID(int = uuid.getnode()).hex[-12:]                          # uuid.uuid4().hex
                
                ##server name:"server_[mac_id]"
                self.server_name = "server_%s" % (uuid.UUID(int = uuid.getnode()).hex[-12:])
                
                ##create default config
                parser.set("DEFAULT", "server",      self.server)
                parser.set("DEFAULT", "rack",        self.rack)
                parser.set("DEFAULT", "server_name", self.server_name)
                
                with io.open(self.server_info, "wb") as config:
                    ##write & truncate & binary
                    parser.write(config)            
                
            else:
                parser.read(self.server_info)
                self.server      = parser.get("DEFAULT", "server").strip()
                self.rack        = parser.get("DEFAULT", "rack").strip()
                self.server_name = parser.get("DEFAULT", "server_name").strip()
                

        self.log_file = os.path.join(self.log_path,     "%s-%s.log"%(self.domain, self.node))
        self.out_file = os.path.join(self.log_path,     "%s-%s.out"%(self.domain, self.node))
        self.pidfile  = os.path.join(self.running_path, "%s-%s.pid"%(self.domain, self.node))
        self.config_loaded = True
        
        return True

    def modifyService(self, service_name, domain):        
        self.node = service_name
        self.domain = domain
        parser = ConfigParser()
        parser.set("DEFAULT", "domain", self.domain)
        parser.set("DEFAULT", "node", self.node)
        parser.set("DEFAULT", "ip", "")
        parser.set("DEFAULT", "group_ip", self.group_ip)
        parser.set("DEFAULT", "group_port", self.group_port)
        with io.open(self.config_file, "wb") as config:
            ##write & truncate & binary
            parser.write(config)
        return True

    def modifyServer(self, name, rack):  
        self.service_name = name
        self.rack = rack
        parser = ConfigParser()
        parser.set("DEFAULT", "server",      self.server)
        parser.set("DEFAULT", "rack",        self.rack)
        parser.set("DEFAULT", "server_name", self.server_name)
        with io.open(self.server_info, "wb") as config:
            ##write & truncate & binary
            parser.write(config)
        return True

    def createService(self):
        """
        create service instance, must override
        """
        pass
            
    def start(self):
        if not self.loadConfig():
            self.console("<ServiceProxy>load config fail from file '%s'"%(
                self.config_file))
            return False
        self.attachLogger()        
        self.service = self.createService()
        if not self.service:
            self.console("<ServiceProxy>create service instance fail")
            return False
        if not self.service.start():
            self.console("<ServiceProxy>start service fail")
            return False
        self.writeProcess()   
        self.console("<ServiceProxy>start service success, domain '%s', node '%s'"%(self.domain, self.node))
        self.redirectOutput()
        return True
            
    def stop(self):
        if self.service:
            self.service.stop()
        self.eraseProcess()
        self.console("<ServiceProxy>stop service success")
        return
    
    def getVersion(self):
        if not self.service:
            return "service version not available"
        else:
            return self.service.getVersion()

    def console(self, content):
        ##output to current console
        print content
##        self.logger.write(content)

    def writeProcess(self):
        ##write pid into pidfile
        pid = os.getpid()
        cmd = self.getProcessCommand(pid)
        file(self.pidfile, 'w+').write("%d:%s\n"%(pid, cmd))
        self.console("<ServiceProxy>pid file %s created, pid %d, cmd '%s'"%(
            self.pidfile, pid, cmd))
        
    def getPID(self):
        if not os.path.exists(self.pidfile):
            return -1
        content = file(self.pidfile,'r').read().strip().split(':')
        if 2 != len(content):
            return -1
        return int(content[0])
    
    def eraseProcess(self):
        if os.path.exists(self.pidfile):
            os.remove(self.pidfile)
            self.console("<ServiceProxy>pid file %s removed"%(self.pidfile))

    def isProcessRunning(self):
        if not self.config_loaded:
            self.loadConfig()
            
        if not os.path.exists(self.pidfile):
            return False
        
        content = file(self.pidfile,'r').read().strip().split(':')
        if 2 != len(content):
            return False
        
        pid = int(content[0])
        cmd = content[1]
        current_cmd = self.getProcessCommand(pid)
        if cmd != current_cmd:
            self.console("<ServiceProxy>pid cmd dismatched, pid '%d', cmd '%s'/'%s'"%(
                pid, cmd, current_cmd))
            return False
        return True

    def getProcessCommand(self, pid):
        path = os.path.join("/proc", str(pid), "cmdline")
        if not os.path.exists(path):
            return ""
        return open(path, "rb").read()
