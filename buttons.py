import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class ToggleButtonWidget:
    def __init__(self, label, action):
        self.action = action
        
        button = gtk.Switch()
        button.connect("notify::active", self.on_activated)

        self.container = gtk.VBox(False, 0)

        self.container.pack_start(gtk.Label(label), False, True, 5)
        self.container.pack_start(button, False, True, 5)

        self.container.show_all()

    def widget(self):
        return self.container

    def on_activated(self, switch, gparam):
        active = switch.get_active()
        print "ACTIVE:", active
