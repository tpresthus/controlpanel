import subprocess
import gi
from gi.repository import GObject as gobject
    
STATE_ON = "on"
STATE_OFF = "off"

class SimpleScriptWithArgument:
    def __init__(self, script, activate_args=[], deactivate_args=[]):
        self.script = script
        self.activate_args = activate_args
        self.deactivate_args = deactivate_args

    def action(self, state, callback=None):
        args = self.get_command(state)
        p = subprocess.Popen(args, 
                stdin=subprocess.PIPE, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE)

        if not callback:
            return

        gobject.timeout_add(250, self.poll_result, 
                {"process": p, "callback": callback})

    def poll_result(self, param):
        p = param["process"]
        callback = param["callback"]

        retcode = p.poll()

        if retcode == None:
            # Process hasn't terminated yet, keep polling
            return True

        success = retcode == 0
        callback(success)

        # Process has terminated. Stop polling
        return False

    def get_command(self, state):
        command = [self.script]
        command.extend(self.get_args(state))

        return command

    def get_args(self, state):
        if state == STATE_ON:
            return self.activate_args
        elif state == STATE_OFF:
            return self.deactivate_args

        return []
