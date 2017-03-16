# -*- encoding: utf-8 -*-
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class TempWidget:
    def __init__(self, filename):
        self.filename = filename
        self.temperature = self.read_temperature()

        self.container = gtk.VBox(False, 10)
        self.create_heading()
        self.create_controls()

        self.set_temperature(self.temperature)
        self.container.show_all()

    def create_heading(self):
        label = gtk.Label()
        label.set_use_markup(True)
        label.set_markup("<span weight='bold' font='16'>Temperatur:</span>")

        self.container.pack_start(label, False, False, 5)

    def create_controls(self):
        controls = gtk.HBox(False, 10)

        button = gtk.Button("-")
        button.connect("clicked", self.on_sub_clicked)
        controls.pack_start(button, True, True, 50)
        
        self.temperature_label = gtk.Label()
        controls.pack_start(self.temperature_label, True, True, 0)

        button = gtk.Button("+")
        button.connect("clicked", self.on_add_clicked)
        controls.pack_start(button, True, True, 50)

        self.container.pack_start(controls, False, False, 10)

    def on_sub_clicked(self, button):
        self.set_temperature(self.temperature - 1)
        self.write_temperature()

    def on_add_clicked(self, button):
        self.set_temperature(self.temperature + 1)
        self.write_temperature()
    def set_temperature(self, temperature):
        self.temperature = temperature

        self.temperature_label.set_use_markup(True)
        self.temperature_label.set_markup("<span weight='bold' font='26'>%.0f° C</span>" % temperature)

    def widget(self):
        return self.container

    def write_temperature(self):
        f = open(self.filename, "w")
        f.write("%d" % self.temperature)
        f.close()

    def read_temperature(self):
        try:
            f = open(self.filename, "r")
            text = f.read().rstrip('\n')
            f.close()

            return float(text)
        except:
            return 0.0;
