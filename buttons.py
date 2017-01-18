import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

STATE_ON = "on"
STATE_OFF = "off"

class SwitchWidget:
    def __init__(self, label, action):
        self.pending = False
        self.action = action
        
        button = gtk.Switch()
        button.connect("state-set", self.on_state_set)

        self.container = gtk.VBox(False, 0)

        self.container.pack_start(gtk.Label(label), False, True, 5)
        self.container.pack_start(button, False, True, 5)

        self.container.show_all()

    def widget(self):
        return self.container
    
    def on_state_set(self, switch, state):
        if not self.action or self.pending:
            self.pending = False
            switch.set_state(state)

            return True

        self.invoke_action(state, switch)
        return True

    def invoke_action(self, active, switch):
        state = STATE_ON if active else STATE_OFF
        self.action(state, 
                callback=lambda success: self.on_callback(switch, active, success))
        
    def on_callback(self, switch, active, success):
        if success:
            switch.set_state(active)
        else:
            self.pending = True
            switch.set_state(not active)
            switch.set_active(not active)
