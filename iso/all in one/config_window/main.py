#!/usr/bin/python
import sys
import gtk
import cairo
import glib

from config_win import *

class MainWindow(gtk.Window):
	
	def __init__(self):
		super(MainWindow, self).__init__()

		self.set_title("ZhiCloud")
		self.fullscreen()
		self.connect("destroy", gtk.main_quit)
		
		screen = self.get_screen()
		width = screen.get_width()
		height = screen.get_height()
		main_bg = gtk.Image()
		main_bg.set_from_file("resource/main_bg.png")
		
		fix = gtk.Fixed()
		config = ConfigWindow()
		fix.put(main_bg, 0, 0)
		fix.put(config, (width-583)/2, (height-700)/2)
		self.add(fix)

		self.set_decorated(True)
		self.show_all()
		
		for one in config.items:
			one.hide()
		config.items[config.current_win].show()

MainWindow()
gtk.main()
