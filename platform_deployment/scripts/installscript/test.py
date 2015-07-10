import os,sys
import sys
import io
from ConfigParser import *
import termios
import tty
from install_progress import *

import socket
import re

def test():
    service="data_server"
    configparser = SafeConfigParser()
    configparser.read("/home/zhicloud/%s/node.conf"%service)
    domain=configparser.get("DEFAULT", "domain")
    group_ip=configparser.get("DEFAULT", "group_ip")
    group_port=configparser.get("DEFAULT", "group_port")
    print ("The %s default configure:domain=%s,group_ip=%s,group_port=%s"%(service,domain,group_ip,group_port))
test()
