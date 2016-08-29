from yapsy.IPlugin import IPlugin
from subprocess32 import check_output
import os

enabled = True

def write_command(message, arguments='type --file -',
                  executable=None):
    with os.popen('%s %s' % (executable, arguments), 'w') as fd:
        fd.write(message)

def paste(text='default'):
    write_command(text, arguments='-b', executable='xsel')
    # server.key_press(key="v", modifiers=("control"))

def copy():
    text = check_output("xsel", shell=True)
    return text

class CopypastePlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(paste)
        server.register_function(copy)
