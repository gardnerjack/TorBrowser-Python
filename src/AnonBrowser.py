from subprocess import call, getoutput, DEVNULL
import os
import time

import socks
import socket
import requests

from bs4 import BeautifulSoup

from stem import Signal
from stem.control import Controller
from stem.connection import authenticate_password, authenticate_none

class AnonBrowser(object):

    def __init__(self, limit=5):
        self.num_requests = 0
        self.request_limit = limit

        self.tor_port = 9050
        self.tor_host = "localhost"
        self.ctrl_port = 9051
        
        self.TorController = None
        self._initTorController()

        self.ctrl_pass = None
        self._set_ctrl_pass(self.ctrl_pass)
        self._initSocks()

        self.ip = self.check_ip()

    def _initTorController(self):
        try:
            self.TorController = Controller.from_port(port=self.ctrl_port)
        except Exception as e:
            print("Tor probably isn't running")
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
        elif "TOR_CTRL_PASS" in os.environ:
            self.ctrl_pass = os.environ["TOR_CTRL_PASS"]

    def _newCircuit(self):
        if self.ctrl_pass:
            authenticate_password(self.TorController, self.ctrl_pass)
        else:
            authenticate_none(self.TorController)
        self.TorController.signal(Signal.NEWNYM)

    def _rotate_ip(self):
        attempts = 0
        new_ip = None
        while attempts < 5:
            self._newCircuit()
            new_ip = self.check_ip
            if new_ip == self.ip:
                print("IP did not successfully rotate. Retrying ...")
                time.sleep(1)
                attempts += 1
            else:
                self.ip = new_ip
                print("New IP: {}".format(self.ip))
                break

    def _update_requests(self):
        self.num_requests += 1
        if self.num_requests > self.request_limit:
            self._rotate_ip()
            self.num_requests = 0

    def check_ip(self):
        return requests.get("http://www.icanhazip.com").text[:-2]

    def get(self, url):
        page = requests.get(url)
        return BeautifulSoup(page.content, parser='html_parser')
