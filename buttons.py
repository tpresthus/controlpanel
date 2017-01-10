import pygtk
pygtk.require("2.0")
import gtk

class ToggleButtonWidget:
    def __init__(self, label, action):
        self.action = action
        self.button = gtk.ToggleButton(label)

        self.button.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#0f0'))
        self.button.modify_bg(gtk.STATE_ACTIVE, gtk.gdk.Color('#0f0'))
        self.button.modify_bg(gtk.STATE_PRELIGHT, gtk.gdk.Color('#0f0'))
        self.button.modify_bg(gtk.STATE_SELECTED, gtk.gdk.Color('#0f0'))
        self.button.modify_bg(gtk.STATE_INSENSITIVE, gtk.gdk.Color('#0f0'))

        self.button.connect("toggled", self.on_toggled)
        self.button.show()

    def widget(self):
        return self.button

    def on_toggled(self, data):
        active = self.button.get_active()
        print "TOGGLED:", active
