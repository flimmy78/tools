#!/usr/bin/python

import sys
import gtk
import glib
import cairo

from toggle_button import *
from image_button import *
from radio_button import *
from get_nic_info import *

class NetConfigWin(gtk.VBox):
	def __init__(self):
		super(NetConfigWin, self).__init__()
		
		nic_info_list = get_all_info()
		mac_label = gtk.Label("")
		if len(nic_info_list) != 0:
			mac_str = "MAC: " + nic_info_list[0].mac
			mac_label.set_text(mac_str)

		auto_radio = RadioButton("/home/zhicloud/config_window/resource/radiobtn_check.png","/home/zhicloud/config_window/resource/radiobtn_uncheck.png", 20, 20, True, RadioBtnType.auto_btn)
		manual_radio  = RadioButton("/home/zhicloud/config_window/resource/radiobtn_check.png","/home/zhicloud/config_window/resource/radiobtn_uncheck.png", 20, 20, False, RadioBtnType.manual_btn)
		auto_radio.add_group(manual_radio)
		manual_radio.add_group(auto_radio)
		auto_get_label = gtk.Image()
		manual_get_label = gtk.Image()
		auto_get_label.set_from_file("/home/zhicloud/config_window/resource/auto_get_label.png")
		manual_get_label.set_from_file("/home/zhicloud/config_window/resource/manual_get_label.png")
		
		ip_label = gtk.Image()
		netmask_label = gtk.Image()
		gateway_label = gtk.Image()
		dns_label = gtk.Image()
		ip_label.set_from_file("/home/zhicloud/config_window/resource/ip_label.png")
		netmask_label.set_from_file("/home/zhicloud/config_window/resource/netmask_label.png")
		gateway_label.set_from_file("/home/zhicloud/config_window/resource/gateway_label.png")
		dns_label.set_from_file("/home/zhicloud/config_window/resource/dns_label.png")

		self.ip_input = gtk.Entry()
		self.netmask_input = gtk.Entry()
		self.gateway_input = gtk.Entry()
		self.dns_input = gtk.Entry()
		self.disable_editbox()

		next_btn = ImageButton("/home/zhicloud/config_window/resource/next_btn_normal.png", "/home/zhicloud/config_window/resource/next_btn_clicked.png", "/home/zhicloud/config_window/resource/next_btn_over.png", 131, 34, self.next_clicked_callback)
	
		nic_info_list = get_all_info()
		self.nic_name = ""
		if len(nic_info_list) != 0:
			self.nic_name = nic_info_list[0].name
			self.ip_input.set_text(nic_info_list[0].ip)
			self.netmask_input.set_text(nic_info_list[0].netmask)
			self.gateway_input.set_text(nic_info_list[0].default_gateway)
			self.dns_input.set_text(nic_info_list[0].dns)
		fix = gtk.Fixed()
		fix.put(mac_label, 118, 297)
		fix.put(auto_radio, 118, 330)
		fix.put(auto_get_label, 163, 329)
		fix.put(manual_radio, 343, 330)
		fix.put(manual_get_label, 384, 329)

		fix.put(ip_label, 163, 380)
		fix.put(self.ip_input, 257, 372)
		fix.put(netmask_label, 163, 421)
		fix.put(self.netmask_input, 257, 416)
		fix.put(gateway_label, 163, 464)
		fix.put(self.gateway_input, 257, 457)
		fix.put(dns_label, 163, 508)
		fix.put(self.dns_input, 257, 500)

		fix.put(next_btn, 227, 592)

		self.add(fix)

	def enable_editbox(self):
		self.ip_input.set_editable(True)
                self.ip_input.set_sensitive(True)
                self.netmask_input.set_editable(True)
                self.netmask_input.set_sensitive(True)
                self.gateway_input.set_editable(True)
                self.gateway_input.set_sensitive(True)
                self.dns_input.set_editable(True)
                self.dns_input.set_sensitive(True)

	def disable_editbox(self):
		self.ip_input.set_editable(False)
                self.ip_input.set_sensitive(False)
                self.netmask_input.set_editable(False)
                self.netmask_input.set_sensitive(False)
                self.gateway_input.set_editable(False)
                self.gateway_input.set_sensitive(False)
                self.dns_input.set_editable(False)
                self.dns_input.set_sensitive(False)
	

	def next_clicked_callback(self):
		config_win = self.get_parent().get_parent()
		config_win.current_win += 1
		for one in config_win.items:
			one.hide()
		config_win.items[config_win.current_win].show()
		config_win.module_img.set_from_file("/home/zhicloud/config_window/resource/module_select2.png")
