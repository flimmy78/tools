#/usr/bin/python
import sys
import gtk
import cairo

from net_config_win import *
from module_select_win import *
from domain_config_win import *
from finish_config_win import *

class ConfigWindow(gtk.VBox):
	def __init__(self):
		super(ConfigWindow, self).__init__()
		
		self.items = []
		self.current_win = 0
		self.set_size_request(583, 700);
		bg = gtk.Image()
		bg.set_from_file("/home/zhicloud/config_window/resource/bg.png")
		
		self.net_img = gtk.Image()
		self.net_img.set_from_file("/home/zhicloud/config_window/resource/netconfig2.png")
		self.module_img = gtk.Image()
		self.module_img.set_from_file("/home/zhicloud/config_window/resource/module_select1.png")
		self.info_img = gtk.Image()
		self.info_img.set_from_file("/home/zhicloud/config_window/resource/info_config1.png")
		fix = gtk.Fixed()
		fix.put(bg, 0, 0)
		fix.put(self.net_img, 115, 110)
		#fix.put(self.module_img, 254, 110)
		#fix.put(self.info_img, 394, 110)

		self.net_win = NetConfigWin()
		fix.put(self.net_win, 0, 0)
		self.module_win = ModuleSelectWin()
		#fix.put(self.module_win, 0, 0)
		self.domain_win = DomainConfigWin()
		#fix.put(self.domain_win, 0, 0)
		self.finish_win = FinishConfigWin()
		fix.put(self.finish_win, 0, 0)
		
		self.items.append(self.net_win)
		#self.items.append(self.module_win)
		#self.items.append(self.domain_win)
		self.items.append(self.finish_win)
		self.current_win = 0
		
		self.add(fix)		
