from subprocess import getoutput, DEVNULL

import socks
import socket

from stem import Signal
from stem.control import Controller

class AnonBrowser(object):

    def __init__(self):
        self.num_requests = 0
        self.tor_port = 9050
        self.tor_host = "localhost"
        self.ctrl_port = 9051
        
        self.TorController = None
        self._initTorController()

        self.ctrl_pass = None
        self._set_ctrl_pass(self.ctrl_pass)
        self._initSocks()

    def _initTorController(self):
        try:
            self.TorController = Controller.from_port(port=self.ctrl_port)
        except Exception as e:
            print("Tor probably isn't running)
            print(e)

    def _initSocks(self):
        try:
            socks.set_default_proxy(socks.SOCKS5, self.tor_host, self.tor_port)
            socket.socket = socks.socksocket
        except Exception as e:
            print("Socket Error")
            print(e)

    def _set_ctrl_pass(self, ctrl_pass):
        if ctrl_pass:
            self.ctrl_pass = ctrl_pass
        else:
            new_pass = getoutput("tor --hash-password \"test_password\"")
            self.ctrl_pass = new_pass

test_browser = TorBrowser()