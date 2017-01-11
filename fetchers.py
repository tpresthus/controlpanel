import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk as gtk
from gi.repository import GObject as gobject

class FileContentFetcher(gobject.GObject):
    def __init__(self, filename, frequency, prefix="", suffix=""):
        gobject.GObject.__init__(self)

        self.filename = filename
        self.frequency = frequency

        self.prefix = prefix
        self.suffix = suffix

        gobject.timeout_add(frequency*1000, self.update)

    def update(self):
        try:
            f = open(self.filename, "r")
            text = f.read().rstrip('\n')
            text = "%s%s%s" % (self.prefix, text, self.suffix)
            f.close()
        except:
            text = "N/A"

        self.emit("updated", text)
        return True

gobject.type_register(FileContentFetcher)
gobject.signal_new("updated", FileContentFetcher, gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))

def from_file(filename, suffix=""):
    return FileContentFetcher(filename, 60, suffix=suffix)
