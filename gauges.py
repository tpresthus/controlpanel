import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk

class Gauges:
    def __init__(self):
        self.container = gtk.VBox(homogeneous=True, spacing=5)
        self.container.show()

        self.rows = list()
        self.last_row = 0

    def create_row(self):
        row = gtk.HBox(homogeneous=True, spacing=5)
        row.show()

        self.container.pack_start(row, True, True, padding=5)
        self.rows.append(row)
        self.last_row = 0

    def add(self, gauge):
        if len(self.rows) == 0 or self.last_row == 3:
            self.create_row()

        row = self.rows[-1]
        row.pack_start(gauge, False, True, padding=5)
        gauge.show()

        self.last_row += 1

    def widget(self):
        return self.container

class LabelWidget:
    def __init__(self, heading, default="", fetcher=None):
        self.container = gtk.VBox(spacing=5)

        self.create_heading(heading)
        self.create_label(default)

        if fetcher:
            fetcher.connect("updated", self.on_update)
            fetcher.update()

        self.container.show()

    def on_update(self, fetcher, data):
        self.set_text(data)

    def widget(self):
        return self.container

    def create_heading(self, heading):
        label = gtk.Label(heading + ":")
        label.show()
        
        self.container.pack_start(label, 
                expand=False, fill=True, padding=5)

    def create_label(self, default=""):
        self.label = gtk.Label()
        self.label.set_use_markup(True)
        self.label.show()
        
        self.set_text(default)
        
        self.container.pack_start(self.label, 
                expand=True, fill=True, padding=5)

    def set_text(self, text):
        self.label.set_markup("<span weight='bold' font='16'>%s</span>" % text)
