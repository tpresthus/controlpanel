import subprocess
import collections
import re

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GObject as gobject
from gi.repository import Gtk as gtk

class Radio:
    """
    Radio rock = http://stream.bauermedia.no:80/radiorock.mp3
    """
    def __init__(self, name, url):
        self.name = name
        self.url = url

        self.player = MediaPlayer()
        self.create_ui()

        self.player.run() # Can be deferred if we don't want to keep mplayer running

    def widget(self):
        return self.container

    def destroy(self, widget=None, data=None):
        self.player.quit()

    def create_ui(self):
        self.container = gtk.VBox(False, 0)

        label = gtk.Label()
        label.set_use_markup(True)
        label.set_markup("<span weight='bold' font='16'>%s</span>" % self.name)

        self.container.pack_start(label, False, False, 0)
        
        self.now_playing_label = gtk.Label()
        self.set_now_playing()
        self.player.connect("title-changed", self.set_now_playing)
        self.container.pack_start(self.now_playing_label, False, False, 0)

        controls = gtk.HBox(False, 0)
        self.container.pack_start(controls, False, False, 0)

        image = gtk.Image.new_from_icon_name("media-playback-start", gtk.IconSize.LARGE_TOOLBAR)
        button = gtk.Button(image=image)
        button.connect("clicked", self.play)
        controls.pack_start(button, False, False, 5)
        
        image = gtk.Image.new_from_icon_name("media-playback-pause", gtk.IconSize.LARGE_TOOLBAR)
        button = gtk.Button(image=image)
        controls.pack_start(button, False, False, 5)
        
        image = gtk.Image.new_from_icon_name("media-playback-stop", gtk.IconSize.LARGE_TOOLBAR)
        button = gtk.Button(image=image)
        controls.pack_start(button, False, False, 5)
        
        button = gtk.VolumeButton()
        controls.pack_start(button, False, False, 5)
        
        self.container.show_all()

    def play(self, ev=None):
        self.player.load_file(self.url)
    
    def set_now_playing(self, source=None, title=None):
        if not title:
            label = "<span></span>"
        else:
            label = "<span weight='bold' font='12'>NOW PLAYING:</span> <span font='12'>%s</span>" % title

        self.now_playing_label.set_use_markup(True)
        self.now_playing_label.set_markup(label)

class MediaPlayer(gobject.GObject):
    def __init__(self):
        gobject.GObject.__init__(self)
        self.process = None
        self.buffer = collections.deque()
        self.buffer_line = ""

    def run(self):
        if self.is_alive():
            return

        self.quit()

        mplayer_path = ["/usr/bin/mplayer", "-slave", "-idle", "-quiet"]
        p = subprocess.Popen(mplayer_path,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)
        
        self.process = p
        gobject.io_add_watch(p.stdout, gobject.IO_IN, self.read_output)
        gobject.timeout_add(500, self.parse_buffer)

    def quit(self):
        self.send_if_alive("quit 0")
        if self.process:
            self.process.terminate()

    def stop(self):
        self.send_if_alive("stop")
    
    def pause(self):
        self.send_if_alive("pause")
    
    def set_volume(self, volume):
        self.send_if_alive("volume %.2f 1" % volume)
    
    def increase_volume(self):
        self.send_if_alive("volume +1")
    
    def decrease_volume(self):
        self.send_if_alive("volume -1")
    
    def mute(self):
        # Can be parameterized with mute 1/0 (on off)
        self.send_if_alive("mute")

    def load_file(self, filename):
        self.send_if_alive("loadfile %s" % filename)

    def send_if_alive(self, command):
        if not self.is_alive():
            return

        self.send(command)

    def is_alive(self):
        if not self.process:
            return False

        retcode = self.process.poll()

        if retcode == None:
            # Process is still running
            return True

        return False

    def send(self, command):
        if not self.is_alive():
            return

        datagram = command + "\n"
        self.process.stdin.write(datagram)

    def read_output(self, source, condition):
        if condition != gobject.IO_IN:
            return True

        char = self.process.stdout.read(1)
        self.buffer.append(char)
        
        return True

    def parse_buffer(self):
        try:
            while True:
                self.buffer_line += self.buffer.popleft()
        except: pass

        if not '\n' in self.buffer_line:
            return True

        index = self.buffer_line.index('\n')
        line = self.buffer_line[:index]
        self.buffer_line = self.buffer_line[index+1:]
        
        self.parse_output(line)

        return True

    def parse_output(self, line):
        if line.startswith('ICY Info:'):
            match = re.search(r"StreamTitle='(.*)';", line)
            title = match.group(1)

            self.emit("title-changed", title)

gobject.type_register(MediaPlayer)
gobject.signal_new("title-changed", MediaPlayer, gobject.SIGNAL_RUN_FIRST,
        gobject.TYPE_NONE, (gobject.TYPE_STRING,))

