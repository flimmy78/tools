#!/usr/bin/python

import gtk
import pygtk
import sys
from ConfigParser import *
import uuid

from toggle_button import *
from image_button import *

class DomainConfigWin(gtk.VBox):
	def __init__(self):
		super(DomainConfigWin, self).__init__()

		domain_name_label = gtk.Label("DOMAIN NAME:")
		self.domain_name_input = gtk.Entry()
		#local_ip_label = gtk.Label("LOCAL IP:")
		self.local_ip_input = gtk.Entry()
		group_ip_label = gtk.Label("GROUP IP:")
		self.group_ip_input = gtk.Entry()
		group_port_label = gtk.Label("GROUP PORT:")
		self.group_port_input = gtk.Entry()
		next_btn = ImageButton("/home/zhicloud/config_window/resource/next_btn_normal.png", "/home/zhicloud/config_window/resource/next_btn_clicked.png", "/home/zhicloud/config_window/resource/next_btn_over.png", 131, 34,self.next_clicked_callback)
		
		
		#config_win = self.get_parent().get_parent()
		#net_win = config_win.net_win
		parser = SafeConfigParser()
		parser.read("/home/zhicloud/installscript/node.conf")
		domain = parser.get("DEFAULT", "domain")
		group_ip = parser.get("DEFAULT", "group_ip")
		group_port = parser.get("DEFAULT", "group_port")
		self.domain_name_input.set_text(domain)
		self.local_ip_input.set_text("")
		self.group_ip_input.set_text(group_ip)
		self.group_port_input.set_text(group_port)
		fix = gtk.Fixed()
		fix.put(domain_name_label, 121, 335)
		fix.put(self.domain_name_input, 230, 335)
		#fix.put(local_ip_label, 121, 380)
		#fix.put(self.local_ip_input, 230, 380)
		fix.put(group_ip_label, 121, 380)
		fix.put(self.group_ip_input, 230, 380)
		fix.put(group_port_label, 121, 425)
		fix.put(self.group_port_input, 230, 425)

		fix.put(next_btn, 215, 530)
		self.add(fix)
		self.connect("expose-event", self.on_expose)
	
	def next_clicked_callback(self):
		config_win = self.get_parent().get_parent()
                config_win.current_win += 1
                for one in config_win.items:
                        one.hide()
                config_win.items[config_win.current_win].show()
                config_win.info_img.set_from_file("/home/zhicloud/config_window/resource/info_config2.png")


	def finish_clicked_callback(self):
		pass

	def on_expose(self, widget, event):
		config_win = self.get_parent().get_parent()
		net_win = config_win.net_win
		local_ip = net_win.ip_input.get_text()
		self.local_ip_input.set_text(local_ip)
