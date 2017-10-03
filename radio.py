import subprocess
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

        self.create_ui()

        self.player = MediaPlayer()
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
        
        label = gtk.Label()
        label.set_use_markup(True)
        label.set_markup("<span weight='bold' font='12'>NOW PLAYING:</span> <span font='12'>%s</span>" % "Walk Idiot Walk - The Hives")

        self.container.pack_start(label, False, False, 0)

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

class MediaPlayer:
    def __init__(self):
        self.process = None

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
        #self.process.communicate(input=datagram)
        self.process.stdin.write(datagram)

    def parse_output(self, line):
        if line.startswith('ICY Info:'):
            match = re.search(r"StreamTitle='(.*)';", line)
            title = match.group(1)

            #TODO: signal title changed
