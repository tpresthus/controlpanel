#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

from gauges import *
from buttons import *
from fetchers import *

def file_gauge(heading, filename, suffix):
    return LabelWidget(heading, "", from_file(filename, suffix)).widget()

class Base:
    def __init__(self):
        self.create_window()
        self.create_lightswitches()
        self.create_gauges()

        self.container.show()
        self.window.show()

    def create_lightswitches(self):
        switches = gtk.HButtonBox()

        button = ToggleButtonWidget("Lys", None)
        switches.pack_start(button.widget(), True, True, 0)

        switches.show()
        self.container.pack_start(switches,
                expand=True, fill=True, padding=0)

    def create_gauges(self):
        gauges = Gauges()

        gauges.add(file_gauge("Ute", "data/temp_ute", "° C"))
        gauges.add(file_gauge("Inne gulv", "data/temp_inne_gulv", "° C"))
        gauges.add(file_gauge("Vann 1", "data/vann1", "%"))
        gauges.add(file_gauge("Inne tak", "data/temp_inne_tak", "° C"))
        gauges.add(LabelWidget("").widget())
        gauges.add(file_gauge("Vann 2", "data/vann2", "%"))

        self.container.pack_start(gauges.widget(),
                expand=False, fill=True, padding=0)

    def create_window(self):
        self.window = gtk.Window()

        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)

        self.window.set_default_size(600, 1024)

        self.container = gtk.VBox(False, 0)
        self.window.add(self.container)
        
    def main(self):
        gtk.main()
    
    def delete_event(self, widet, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()


if __name__ == "__main__":
    base = Base()
    base.main()
