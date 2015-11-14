#!/usr/bin/python

import sys
import gtk
import cairo
import glib

class RadioBtnType:
	auto_btn = 0
	manual_btn = 1
	def __init__(self):
		pass

class RadioButton(gtk.DrawingArea):
	def __init__(self, check_img_name, uncheck_img_name, width, height, is_checked, btn_type):
		super(RadioButton, self).__init__()
		
		self.check_img = cairo.ImageSurface.create_from_png(check_img_name)
		self.uncheck_img = cairo.ImageSurface.create_from_png(uncheck_img_name)
	
		self.width = width
		self.height = height
		self.is_checked = is_checked
		self.btn_type = btn_type
		self.group_btn = []
		
		self.set_size_request(width, height)
		self.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		
		self.connect("button-press-event", self.on_clicked)
		self.connect("expose-event", self.on_expose)

	def add_group(self, other_radio_btn):
		self.group_btn.append(other_radio_btn)
	
	def on_clicked(self, widget, event):
		self.is_checked = True
		self.queue_draw()
		net_win = self.get_parent().get_parent()
		if self.btn_type == RadioBtnType.auto_btn:
			net_win.disable_editbox()
		else:
			net_win.enable_editbox()
		for btn in self.group_btn:
			btn.is_checked = False
			btn.queue_draw()		

	def on_expose(self, widget, event):
                cr = widget.window.cairo_create()
                cr.set_source_rgb(255, 255, 255)
                cr.paint()
                if self.is_checked == True:
                        cr.set_source_surface(self.check_img, 0, 0)
                        cr.paint()
                else:
                        cr.set_source_surface(self.uncheck_img, 0, 0)
			cr.paint()


	def get_check_status(self):
		return self.is_checked
