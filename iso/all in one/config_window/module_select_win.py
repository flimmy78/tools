#!/usr/bin/python

import sys
import gtk
import glib
import cairo

from toggle_button import *
from image_button import *

class ModuleSelectWin(gtk.VBox):
	def __init__(self):
		super(ModuleSelectWin, self).__init__()

		self.ds_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
		self.ds_label = gtk.Label("DATA_SERVER")
		
		self.cs_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.cs_label = gtk.Label("CONTROL_SERVER")
		
		self.web_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.web_label = gtk.Label("WEB_TERMINAL")
		
		self.ir_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.ir_label = gtk.Label("INTELIGENT_ROUTE")

		self.nc_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.nc_label = gtk.Label("NODE_CLIENT")

		self.storage_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.storage_label = gtk.Label("STORAGE_SERVER")
		
		self.statistic_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.statistic_label = gtk.Label("STATISTIC_SERVER")
		
		self.gateway_checkbtn = ToggleButton("/home/zhicloud/config_window/resource/checkbtn_check.png", "/home/zhicloud/config_window/resource/checkbtn_uncheck.png", 21, 21, False)
                self.gateway_label = gtk.Label("HTTP_GATEWAY")



		next_btn = ImageButton("/home/zhicloud/config_window/resource/next_btn_normal.png", "/home/zhicloud/config_window/resource/next_btn_clicked.png", "/home/zhicloud/config_window/resource/next_btn_over.png", 131, 34, self.next_clicked_callback)

		fix = gtk.Fixed()
		fix.put(self.ds_checkbtn, 201, 300)
		fix.put(self.ds_label, 270, 300)
		fix.put(self.cs_checkbtn, 201, 340)
		fix.put(self.cs_label, 270, 340)
		fix.put(self.web_checkbtn, 201, 380)
		fix.put(self.web_label, 270, 380)
		fix.put(self.nc_checkbtn, 201, 420)
		fix.put(self.nc_label, 270, 420)
		fix.put(self.storage_checkbtn, 201, 460)
                fix.put(self.storage_label, 270, 460)
		fix.put(self.statistic_checkbtn, 201, 500)
                fix.put(self.statistic_label, 270, 500)
		fix.put(self.ir_checkbtn, 201, 540)
                fix.put(self.ir_label, 270, 540)
		fix.put(self.gateway_checkbtn, 201, 580)
                fix.put(self.gateway_label, 270, 580)

		self.checkbtn_list = []
		self.checkbtn_list.append(self.ds_checkbtn)
		self.checkbtn_list.append(self.cs_checkbtn)
		self.checkbtn_list.append(self.web_checkbtn)
		self.checkbtn_list.append(self.nc_checkbtn)
		self.checkbtn_list.append(self.storage_checkbtn)
		self.checkbtn_list.append(self.statistic_checkbtn)
		self.checkbtn_list.append(self.ir_checkbtn)
		self.checkbtn_list.append(self.gateway_checkbtn)

		fix.put(next_btn, 220, 614)
		self.add(fix)
	
	def next_clicked_callback(self):
		has_one_check = False
		for btn in self.checkbtn_list:
			if btn.is_checked == True:
				has_one_check = True
				break
		if has_one_check == False:
			pass

		config_win = self.get_parent().get_parent()
		config_win.current_win += 1
		for one in config_win.items:
			one.hide()
		config_win.items[config_win.current_win].show()
		config_win.info_img.set_from_file("/home/zhicloud/config_window/resource/info_config2.png")
