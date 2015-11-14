#!/usr/bin/python

import sys
import gtk
import cairo
import glib

class StatusEnum():
	normal = 1
	over = 2
	clicked = 3
	def __init__():
		pass

class ImageButton(gtk.DrawingArea):
	def __init__(self, normal_img_name, clicked_img_name, over_img_name, width, height, callback=None):
		super(ImageButton, self).__init__()
		
		self.normal_img = cairo.ImageSurface.create_from_png(normal_img_name)
		self.clicked_img = cairo.ImageSurface.create_from_png(clicked_img_name)
		self.over_img = cairo.ImageSurface.create_from_png(over_img_name)
		self.width = width
		self.height = height
		self.status = StatusEnum.normal
		self.callback = callback
		
		self.set_size_request(width, height)
		self.set_events(gtk.gdk.BUTTON_PRESS_MASK|gtk.gdk.BUTTON_RELEASE_MASK|gtk.gdk.ENTER_NOTIFY_MASK|gtk.gdk.LEAVE_NOTIFY_MASK)
		
		self.connect("button-press-event", self.on_clicked)
		self.connect("button-release-event", self.on_released)
		self.connect("enter-notify-event", self.on_enter)
		self.connect("leave-notify-event", self.on_leave)
		self.connect("expose-event", self.on_expose)
	
	def on_clicked(self, widget, event):
		self.status = StatusEnum.clicked
		self.queue_draw()
		if self.callback != None:
			self.callback()
	
	def on_released(self, widget, event):
		self.status = StatusEnum.normal
		self.queue_draw()

	def on_enter(self, widget, event):
		self.status = StatusEnum.over
		self.queue_draw()
	
	def on_leave(self, widget, event):
		self.status = StatusEnum.normal
		self.queue_draw()		

	def on_expose(self, widget, event):
                cr = widget.window.cairo_create()
                cr.set_source_rgb(255, 255, 255)
                cr.paint()
                if self.status == StatusEnum.clicked:
                        cr.set_source_surface(self.clicked_img, 0, 0)
                        cr.paint()
                elif self.status == StatusEnum.over:
                        cr.set_source_surface(self.over_img, 0, 0)
			cr.paint()
		else:
			cr.set_source_surface(self.normal_img, 0, 0)
			cr.paint()
