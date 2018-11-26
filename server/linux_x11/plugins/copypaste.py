from yapsy.IPlugin import IPlugin
from subprocess32 import check_output, Popen, PIPE
import os

enabled = True


def copy(text):
    with os.popen('python -m pyperclip -c', 'w') as fd:
        fd.write(text)


def paste():
    text = check_output(['python', '-m', 'pyperclip', '-p'])
    return text


class CopypastePlugin(IPlugin):
    def register_rpcs(self, server):
        server.register_function(paste)
        server.register_function(copy)

