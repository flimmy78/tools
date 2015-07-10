# -*- coding: cp936 -*-
import ConfigParser
import os


def GetValue(cfg, Section, Key, Default = ""):
        try:
            value = cfg.get(Section, Key)
        except:
            value = Default
        return value


config = ConfigParser.ConfigParser()

config.read('/usr/local/zhicloud/zhicloud.conf')

if GetValue(config,"service","data_server") == "enable":
    print "START Data Server..."
    os.system("cd /home/zhicloud/data_server && ./data_server restart")
    print ""
    print ""

if GetValue(config,"service","control_server") == "enable":
    print "START Control Server..."
    os.system("cd /home/zhicloud/control_server && ./control_server restart")
    print ""
    print ""

if GetValue(config,"service","storage_server") == "enable":
    print "START Storage Server..."
    os.system("cd /home/zhicloud/storage_server && ./storage_server restart")
    print ""
    print ""

if GetValue(config,"service","statistic_server") == "enable":
    print "START Statistic Server..."
    #os.system("cd /home/zhicloud/statistic_server && ./main restart")
    print ""
    print ""

if GetValue(config,"service","node_client") == "enable":
    print "START Node Client.."
    os.system("cd /home/zhicloud/node_client && ./node_client restart")
    print ""
    print ""
    
if GetValue(config,"service","intelligent_router") == "enable":
    print "START Intelligent Router........"
    os.system("cd /home/zhicloud/intelligent_router && ./intelligent_router restart")
    print ""
    print ""
