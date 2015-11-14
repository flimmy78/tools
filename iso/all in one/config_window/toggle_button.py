#!/usr/bin/python

import sys
import gtk
import cairo
import glib

class ToggleButton(gtk.DrawingArea):
	def __init__(self, check_img_name, uncheck_img_name, width, height, is_checked):
		super(ToggleButton, self).__init__()
		
		self.check_img = cairo.ImageSurface.create_from_png(check_img_name)
		self.uncheck_img = cairo.ImageSurface.create_from_png(uncheck_img_name)
	
		self.width = width
		self.height = height
		self.is_checked = is_checked
		
		self.set_size_request(width, height)
		self.set_events(gtk.gdk.BUTTON_PRESS_MASK)
		
		self.connect("button-press-event", self.on_clicked)
		self.connect("expose-event", self.on_expose)
	
	def on_clicked(self, widget, event):
		self.is_checked = not self.is_checked
		self.queue_draw()		

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
