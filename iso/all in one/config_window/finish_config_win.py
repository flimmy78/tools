import gtk
import sys
import os
import io
import uuid
from ConfigParser import *
from globalvar import *

from image_button import *

class FinishConfigWin(gtk.VBox):
	def __init__(self):
		super(FinishConfigWin, self).__init__()
		self.is_ds_checked = True
		self.is_cs_checked = True
		self.is_web_checked = True
		self.is_ir_checked = False
		self.is_nc_checked = False
		self.is_storage_checked = True
		self.is_statistic_checked = False
		self.is_gateway_checked = True
		self.installstr = " "

		finish_img = gtk.Image()
		finish_img.set_from_file("/home/zhicloud/config_window/resource/finish_bg.png")
		self.url_label = gtk.Label("")
		
		finish_btn = ImageButton("/home/zhicloud/config_window/resource/finish_btn_normal.png", "/home/zhicloud/config_window/resource/finish_btn_clicked.png", "/home/zhicloud/config_window/resource/finish_btn_over.png", 131, 34, self.btn_clicked_callback)
		fix = gtk.Fixed()
		fix.put(finish_img, 202, 297)
		fix.put(self.url_label, 72, 550)
		fix.put(finish_btn, 220, 608)
		self.add(fix)
		self.connect("expose-event", self.on_expose)
	
	def on_expose(self, widget, event):
		config_win = self.get_parent().get_parent()
		net_win = config_win.net_win
		local_ip = net_win.ip_input.get_text()
		self.web_addr = "http:\/\/" + local_ip + ":8080\/CloudDeskTopMS\/"

                if self.is_web_checked == True:
			url_str = "Please visit the url http://" + local_ip + ":8080/CloudDeskTopMS to operate!"
                	self.url_label.set_text(url_str)

	def btn_clicked_callback(self):
		config_win = self.get_parent().get_parent()
		self.get_option()
		cmdstr = "sh /home/zhicloud/installscript/installconfig " + self.installstr
		os.system(cmdstr)
		os.system("sh /home/zhicloud/installscript/localsed.sh 's/id:5:initdefault:/id:3:initdefault:/g' /etc/inittab")
		os.system("shutdown -r now")
		#os.system("telinit 3")
		sys.exit()

	def get_option(self):
		self.set_group()
	
	def set_group(self):
		config_win = self.get_parent().get_parent()
		net_win = config_win.net_win
		netmask = net_win.netmask_input.get_text()
		gateway = net_win.gateway_input.get_text()
		dns = net_win.dns_input.get_text()
		nic_name = net_win.nic_name
		net_win = config_win.net_win
		local_ip = net_win.ip_input.get_text()

		parser = SafeConfigParser()
		parser.read("/home/zhicloud/installscript/node.conf")
		parser.set("DEFAULT", "domain", "zhicloud_aio")
		parser.set("DEFAULT", "group_ip", "224.6.9.9")
		parser.set("DEFAULT", "group_port", "5678")
		fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
		parser.write(fd)
		fd.close()
		self.setip(nic_name, local_ip, netmask, gateway, dns)
		
		if self.is_ds_checked == True:
			self.installstr = self.installstr + "data_server "
                	node ="data_server"
                	parser = SafeConfigParser()
               		parser.read("/home/zhicloud/installscript/node.conf")
                	parser.set("DEFAULT", "node", node)
                	parser.set("DEFAULT", "ip", local_ip)
                	fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
                	parser.write(fd)
                	fd.close()
                	os.system("mkdir -p /var/zhicloud/config/data_server")
                	os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/data_server/")
		
		if self.is_cs_checked == True:
			self.installstr = self.installstr + "control_server "
			mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
			node = "control_server_%s"%(mac_string)
			parser = SafeConfigParser()
			parser.read("/home/zhicloud/installscript/node.conf")
			parser.set("DEFAULT", "node", node)
			parser.set("DEFAULT", "ip", "")
			fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
			parser.write(fd)
			fd.close()
			os.system("mkdir -p /var/zhicloud/config/control_server")
			os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/control_server/")
		
		if self.is_storage_checked == True:
			self.installstr = self.installstr + "storage_server "
			mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
			node = "storage_server_%s"%(mac_string)
			parser = SafeConfigParser()
			parser.read("/home/zhicloud/installscript/node.conf")
			parser.set("DEFAULT", "node", node)
			parser.set("DEFAULT", "ip", "")
			fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
			parser.write(fd)
			fd.close()
			os.system("mkdir -p /var/zhicloud/config/storage_server")
			os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/storage_server/")
		
		if self.is_statistic_checked == True:
			self.installstr = self.installstr + "static_server "
			mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
			node = "static_server_%s"%(mac_string)
			parser = SafeConfigParser()
			parser.read("/home/zhicloud/installscript/node.conf")
			parser.set("DEFAULT", "node", node)
			parser.set("DEFAULT", "ip", "")
			fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
			parser.write(fd)
			fd.close()
			os.system("mkdir -p /var/zhicloud/config/static_server")
			os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/static_server/")

		
		if self.is_nc_checked == True:
			self.installstr = self.installstr + "node_client "
			mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
			print mac_string
			node = "node_client_%s"%(mac_string)
			parser = SafeConfigParser()
			parser.read("/home/zhicloud/installscript/node.conf")
			parser.set("DEFAULT", "node", node)
			parser.set("DEFAULT", "ip", "")
			fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
			parser.write(fd)
			fd.close()
			os.system("mkdir -p /var/zhicloud/config/node_client")
			os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/node_client/")
		
		if self.is_ir_checked == True:
			self.installstr = self.installstr + "intelligent_router "
			mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
			node = "intelligent_router_%s"%(mac_string)
			parser = SafeConfigParser()
			parser.read("/home/zhicloud/installscript/node.conf")
			parser.set("DEFAULT", "node", node)
			parser.set("DEFAULT", "ip", "")
			fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
			parser.write(fd)
			fd.close()
			os.system("mkdir -p /var/zhicloud/config/intelligent_router")
			os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/intelligent_router/")
		
		if self.is_gateway_checked == True:
			self.installstr = self.installstr + "http_gateway "
			mac_string = uuid.UUID(int = uuid.getnode()).hex[-12:]
			node = "http_gateway_%s"%(mac_string)
			parser = SafeConfigParser()
			parser.set("DEFAULT", "ip", "")
			parser.read("/home/zhicloud/installscript/node.conf")
			parser.set("DEFAULT", "node", node)
			fd = io.open("/home/zhicloud/installscript/node.conf", 'wb')
			parser.write(fd)
			fd.close()
			os.system("mkdir -p /var/zhicloud/config/http_gateway")
			os.system("cp /home/zhicloud/installscript/node.conf /var/zhicloud/config/http_gateway/")
		
		if self.is_web_checked == True:
			self.installstr = self.installstr + "web_server "
			os.system("mkdir -p /tmp/_tmp_web_/")
			os.system("cp /home/zhicloud/apache-tomcat-7.0.64/webapps/CloudDeskTopMS.war /tmp/_tmp_web_")
			os.system("cd /tmp/_tmp_web_ && jar -xf ./CloudDeskTopMS.war")
			cmd = r'sed -i "/this_system/{N;N;s/\(this_system[^\n]*\n[^\n]*\n[^h]*\)\(http[^\n]*\)/\1%s/}" /tmp/_tmp_web_/META-INF/app-properties.xml' % self.web_addr
        		os.system(cmd)
			os.system("cd /tmp/_tmp_web_ && jar -cf ./CloudDeskTopMS.war ./*")
			os.system("cd /tmp/_tmp_web_ && mv -f ./CloudDeskTopMS.war /home/zhicloud/apache-tomcat-7.0.64/webapps/")

	def setip(self, nic_name, ip, mask, gateway, dns):
		if nic_name == "eth0":
			os.system("sh /home/zhicloud/installscript/localsed.sh 's/BOOTPROTO.*$/BOOTPROTO=static/g' /etc/sysconfig/network-scripts/ifcfg-eth0")
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/IPADDR.*$/d' IPADDR=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%ip)
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/NETMASK.*$/d' NETMASK=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%mask)
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/ONBOOT.*$/d' ONBOOT=yes /etc/sysconfig/network-scripts/ifcfg-eth0")
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/GATEWAY.*$/d' GATEWAY=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%gateway)
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/DNS1.*$/d' DNS1=%s /etc/sysconfig/network-scripts/ifcfg-eth0"%dns)
		elif nic_name == "em1":
			os.system("sh /home/zhicloud/installscript/localsed.sh 's/BOOTPROTO.*$/BOOTPROTO=static/g' /etc/sysconfig/network-scripts/ifcfg-em1")
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/IPADDR.*$/d' IPADDR=%s /etc/sysconfig/network-scripts/ifcfg-em1"%ip)
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/NETMASK.*$/d' NETMASK=%s /etc/sysconfig/network-scripts/ifcfg-em1"%mask)
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/ONBOOT.*$/d' ONBOOT=yes /etc/sysconfig/network-scripts/ifcfg-em1")
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/GATEWAY.*$/d' GATEWAY=%s /etc/sysconfig/network-scripts/ifcfg-em1"%gateway)
			os.system("sh /home/zhicloud/installscript/localupdate.sh '/DNS1.*$/d' DNS1=%s /etc/sysconfig/network-scripts/ifcfg-em1"%dns)

            	#set static route
            	file_route=open('/etc/sysconfig/static-routes','w')
            	route="0.0.0.0/0 via "+gateway
            	file_route.write(route)
            	file_route.close()
		os.system("sh /home/zhicloud/installscript/add_bridge.sh")
		os.system("service network restart")

