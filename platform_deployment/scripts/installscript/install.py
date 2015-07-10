import os,sys
import sys
import io
from ConfigParser import *
import termios
import tty
import uuid
from install_progress import *

import socket
import re
import globalvar

def ipFormatChk(ip_str):
    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    if re.match(pattern, ip_str):
       return True
    else:
       return False
def valid_ip(address):
    if ipFormatChk(address):
       try: 
           socket.inet_aton(address)
           return True
       except:
           return False
    else:
       return False

term = io.open(sys.stdin.fileno(),'r')
def getchar():
    sys.stdin.flush()
    fd = term.fileno()
    old = termios.tcgetattr(fd)
    new = termios.tcgetattr(fd)
    new[3] &= ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, new)
    c = None
    try:
        c = term.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)
        #term.close()
    return c

def user_input(value = "1234567890.abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    chars = []
    while True:
        newChar = getchar()
        if newChar in '\r\n':
            print ''
            break
        elif newChar == '\b' or newChar == '\x7f':
            if chars:
                chars[-1] = ' '
                sys.stdout.write('\r')
                sys.stdout.write(''.join(chars))
                sys.stdout.write('\r')
                del chars[-1]
                sys.stdout.write(''.join(chars))
                
        elif newChar in value:
            chars.append(newChar)
            sys.stdout.write(newChar)
        else:
            #print newChar
            continue
        sys.stdout.flush()
    return ''.join(chars)
def set_group():
    while True:
        print "Please input domain:"
        domain=user_input("1234567890._abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
        break
    while True:
        print "Please input group IP:"
        group_ip=user_input("1234567890.")
        if valid_ip(group_ip):
            break
        else:
            print "\033[0;31mInvalid group IP\033[0m,please confirm your input IP."
    while True:
        print "Please input group Port:"
        group_port=user_input("1234567890")
        break
    print "Confirm your Input:"
    print "domain=%s"%domain
    print "group_ip=%s"%group_ip
    print "group_port=%s"%group_port
    print "save it ?Y/N"
    line  = user_input("YNyn")
    if len(line) > 0 and line[0] in 'yY':
        #parser = ConfigParser()        
        parser = SafeConfigParser()
        parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
        parser.set("DEFAULT", "domain", domain)
        parser.set("DEFAULT", "group_ip", group_ip)
        parser.set("DEFAULT", "group_port", group_port)
        fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
        parser.write(fd)
        fd.close()

        mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
        node = "control_server_%s"%(mac_string)
        parser = SafeConfigParser()
        parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
        parser.set("DEFAULT", "node", node)
        fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
        parser.write(fd)
        fd.close()
        os.system("mkdir -p /var/zhicloud/config/control_server")
        os.system("cp %s/installscript/node.conf /var/zhicloud/config/control_server/"%globalvar.InstallPath)


        mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
        node = "storage_server_%s"%(mac_string)
        parser = SafeConfigParser()
        parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
        parser.set("DEFAULT", "node", node)
        fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
        parser.write(fd)
        fd.close()
        os.system("mkdir -p /var/zhicloud/config/storage_server")
        os.system("cp %s/installscript/node.conf /var/zhicloud/config/storage_server/"%globalvar.InstallPath)


        mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
        node = "static_server_%s"%( mac_string)
        parser = SafeConfigParser()
        parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
        parser.set("DEFAULT", "node", node)
        fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
        parser.write(fd)
        fd.close()
        os.system("mkdir -p /var/zhicloud/config/static_server")
        #os.system("cp %s/installscript/node.conf %s/static_server/"%(globalvar.InstallPath,globalvar.InstallPath))
        os.system("cp %s/installscript/node.conf /var/zhicloud/config/static_server/"%globalvar.InstallPath)


        mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
        node = "node_client_%s"%( mac_string)
        parser = SafeConfigParser()
        parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
        parser.set("DEFAULT", "node", node)
        fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
        parser.write(fd)
        fd.close()
        #os.system("cp %s/installscript/node.conf %s/node_client/"%(globalvar.InstallPath,globalvar.InstallPath))
        os.system("mkdir -p /var/zhicloud/config/node_client")
        os.system("cp %s/installscript/node.conf /var/zhicloud/config/node_client/"%globalvar.InstallPath)

        mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
        node = "intelligent_router_%s"%(mac_string)
        parser = SafeConfigParser()
        parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
        parser.set("DEFAULT", "node", node)
        fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
        parser.write(fd)
        fd.close()
        os.system("mkdir -p /var/zhicloud/config/intelligent_router")
        os.system("cp %s/installscript/node.conf /var/zhicloud/config/intelligent_router/"%globalvar.InstallPath)
    return True

def setip():
    global ip
    mask = ""
    gateway = ""
    print "***************************"
    print "*        \033[0;32mset ip\033[0m           *"
    print "***************************"
    
    while True :
        print "Please input the ipaddr:"
        ip = user_input("1234567890.")
        if valid_ip(ip):
            break
        else:
            print "\033[0;31mInvalid IP\033[0m,please confirm your input ipaddr,"
    while True :
        print "Please in put the net mask:"
        mask = user_input("1234567890.")
        if valid_ip(mask):

            break
        else:
            print "\033[0;31mInvalid NET Mask\033[0m,please confirm your input net mask,"
            
    while True :
        print "please in put the input gateway:"
        gateway = user_input("1234567890.")
        if valid_ip(gateway):
            break
        else:
            print "\033[0;31mInvalid Gateway\033[0m,,please confirm your input gateway,"
        
    print "confirm your input:"
    print "ipaddr:%s"%ip
    print "mask:%s"%mask
    print "gateway:%s"%gateway
    
    print "save it ?,Y/N"
    line  = user_input("YNyn")
    if len(line) > 0 and line[0] in 'yY':
            os.system("sh %s/installscript/localsed.sh 's/BOOTPROTO.*$/BOOTPROTO=static/g' /etc/sysconfig/network-scripts/ifcfg-eth0"%globalvar.InstallPath)
            os.system("sh %s/installscript/localupdate.sh '/IPADDR.*$/d' IPADDR=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%(globalvar.InstallPath,ip))
            os.system("sh %s/installscript/localupdate.sh '/NETMASK.*$/d' NETMASK=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%(globalvar.InstallPath,mask))
            os.system("sh %s/installscript/localupdate.sh '/GATEWAY.*$/d' GATEWAY=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%(globalvar.InstallPath,gateway))

            #set static route
            file_route=open('/etc/sysconfig/static-routes','w')
            route="0.0.0.0/0 via "+gateway
            file_route.write(route)
            file_route.close()

            os.system("service network restart")
            try:
                ##########set data_server's local ip##########
                node ="data_server"
                parser = SafeConfigParser()
                parser.read("%s/installscript/node.conf"%globalvar.InstallPath)
                parser.set("DEFAULT", "node", node)
                parser.set("DEFAULT", "ip", ip)
                fd = io.open("%s/installscript/node.conf"%globalvar.InstallPath, 'wb')
                parser.write(fd)
                fd.close()
                #os.system("cp %s/installscript/node.conf %s/data_server/"%(globalvar.InstallPath,globalvar.InstallPath))
                os.system("mkdir -p /var/zhicloud/config/data_server")
                os.system("cp %s/installscript/node.conf /var/zhicloud/config/data_server/"%globalvar.InstallPath)
            except:
                print "Config dataserver ipaddr fail"
            return True
    return False
        
def get_option():
    global ip   
    pwd=sys.path[0]
    globalvar.InstallPath=os.path.abspath(os.path.join(pwd,os.pardir))
    while True:    
        installstr=""
        print "please enter the moudle need to install:"
        print "1,Install Data Server:"
        print "2,Install Control Server"
        print "3,Install Storage Server"
        print "4,Install Statistic Server"
        print "5,Install Node client"
        print "6,Install Intelligent router"
        print "7,exit"
        print "You can choose as format:1,2,3,4,5,6"
        print "Note:Node client and Intelligent router can't install on a same server!"
        line  =user_input("1234567,");
        if '5'in line and '6'in line:
            print "\033[0;32mNode client and Intelligent router can't install on a same server!Thank you!\033[0m"
            print ""
            continue
        modules=line.split(',');
        for module in modules:
            if module == '1':
                installstr = installstr + ' data_server'            
            elif module == '2':
                installstr = installstr + ' control_server'
            elif module == '3':
                installstr = installstr + ' storage_server'
            elif module == '4':
                installstr = installstr + ' statistic_server'
            elif module == '5':
                installstr = installstr + ' node_client'
            elif module == '6':
                installstr = installstr + ' intelligent_router'
            elif module == '7':
                print "exit"
                return
            else:
                print "input error! "
                continue
        print "you will install :%s"%installstr
        print "confirm it ,Y/N"
        line  = user_input("YNyn")
        if len(line) > 0 and line[0] in 'yY':
            print "***************************"
            print "   \033[0;32mSet the node configure\033[0m"
            print "***************************"
            configparser = SafeConfigParser()
            configparser.read("%s/installscript/node.conf"%globalvar.InstallPath)
            domain=configparser.get("DEFAULT", "domain")
            group_ip=configparser.get("DEFAULT", "group_ip")
            group_port=configparser.get("DEFAULT", "group_port")
            print ("The default configure:domain=%s,group_ip=%s,group_port=%s"%(domain,group_ip,group_port))
            print "Do you want to set your own configure?Y/N"
            line = user_input("YNyn")
            if len(line) > 0 and line[0] in 'yY':
                set_group();
            if 'data_server' in installstr:
                print "                "
                print "you select to install dataserver,you must config local ip"
                if not setip():
                    continue
                    
            print "\033[?25l"
            print "#############################################"
            print "######\033[0;32mZhicloud service installer Runing\033[0m######"
            print "#############################################"

            try:
                    installStepManager = InstallStepManager()
                    services = installstr.split()
                    for service in services:
                        installStepManager.AddInstallService(service)
                    installStepManager.RunInstallScript()
            except:
                    print "Zhicloud service installer fail"
            print "#############################################"
            print "####\033[0;32mZhicloud service installer Completed\033[0m#####"
            print "#############################################"
            print "\33[?25h"
        
def runinstall():
    os.system("/bin/plymouth --quit")
    os.system("clear")

    get_option()
    
        
runinstall()
