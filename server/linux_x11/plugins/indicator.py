from yapsy.IPlugin import IPlugin

import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3, GObject
import time
import subprocess32
from threading import Thread
from time import sleep

# ON = "/home/tyler/Dropbox/appdata/dragon/indicator/on_icon.png"
# OFF = "/home/tyler/Dropbox/appdata/dragon/indicator/off_icon.png"

def state_png_map(key):
    state_map = {
        'off': '/home/tyler/code/magneto-host/server/linux_x11/plugins/icons/aenea-red.png',
        'on': '/home/tyler/code/magneto-host/server/linux_x11/plugins/icons/aenea-green.png',
        'sleeping': '/home/tyler/code/magneto-host/server/linux_x11/plugins/icons/aenea-yellow.png',
        'idk': '/home/tyler/code/magneto-host/server/linux_x11/plugins/icons/aenea-dark.png'
    }
    return state_map.get(key, state_map['idk'])
    
def reboot_dragon(x):
    print("rebooting dragon")
    subprocess32.Popen(["vboxmanage", "guestcontrol", "dragon", "run", "--username",
        "tyler", "--passwordfile", "/home/tyler/Dropbox/appdata/dragonpass.txt",
        "C:\\Users\\tyler\\Desktop\\reboot.bat", "&"])
    sleep(21)
    print("turning on microphone")
    subprocess32.Popen(["VBoxManage", "controlvm", "dragon", "keyboardputscancode", "1D", "2A", "24",
        "A4", "9D", "AA"])


class Indicator():
    def __init__(self):
        self.app = 'test123'
        self.update_indicator(state_png_map('idk'))
        # the thread:
        # self.update = Thread(target=self.toggle)
        # daemonize the thread to make the indicator stopable
        # self.update.setDaemon(True)
        # self.update.start()

    def create_menu(self):
        menu = Gtk.Menu()
        # menu item 1
        item_1 = Gtk.MenuItem('Reboot dragon')
        item_1.connect('activate', reboot_dragon)
        menu.append(item_1)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def update_indicator(self, status):
        self.status = status
        self.indicator = AppIndicator3.Indicator.new(
            self.app, state_png_map(status),
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)       
        self.indicator.set_menu(self.create_menu())
        # self.indicator.set_label("1 Monkey", self.app)


    # def toggle(self):
    #     t = 2
    #     while True:
    #         time.sleep(1)
    #         mention = str(t)+" Monkeys"
    #         # apply the interface update using  GObject.idle_add()
    #         if self.status==OFF:
    #             status = ON
    #         elif self.status==ON:
    #             status = OFF
    #         GObject.idle_add(
    #             self.update_indicator,
    #             status,
    #             priority=GObject.PRIORITY_DEFAULT
    #             )
    #         t += 1

    def stop(self, source):
        Gtk.main_quit()

def dummy():
    pass

indicator = Indicator()
# # this is where we call GObject.threads_init()
# GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
thread = Thread(target=Gtk.main)
thread.start()
# Gtk.mainloop()

# class IndicatorPlugin(IPlugin):
#     def register_rpcs(self, server):
#         server.register_function(dummy)



class IndicatorPlugin(IPlugin):


    def register_rpcs(self, server):
        server.register_function(self.natlink_microphone_change)
        server.register_function(reboot_dragon)

    @staticmethod
    def natlink_microphone_change(args):
        try:
            indicator.update_indicator(args)
        except Exception as e:
            print 'natlink_microphone_change error: ', e

