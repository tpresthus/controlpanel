import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class ToggleButtonWidget:
    def __init__(self, label, action):
        self.action = action
        self.button = gtk.Switch()

        self.button.connect("notify::active", self.on_activated)
        self.button.show()

    def widget(self):
        return self.button

    def on_activated(self, switch, gparam):
        active = switch.get_active()
        print "ACTIVE:", active
