from subprocess import call, getoutput, DEVNULL
import os
import time

import socks
import socket
import requests

from bs4 import BeautifulSoup

from stem import Signal
from stem.control import Controller
from stem.connection import authenticate


class AnonBrowser(object):

    def __init__(self, limit=5, use_soup=False):
        self.num_requests = 0
        self.request_limit = limit

        self.tor_port = 9050
        self.tor_host = "localhost"
        self.ctrl_port = 9051

        self.TorController = None
        self._initTorController()

        self._initSocks()

        self.ip = self.check_ip()

        self._use_soup = use_soup

    def _initTorController(self):
        try:
            self.TorController = Controller.from_port(port=self.ctrl_port)
        except Exception as e:
            print("Tor probably isn't running")
            print(e)

    def _initSocks(self):
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, self.tor_host, self.tor_port)
        socket.socket = socks.socksocket

    def _newCircuit(self):
        self.TorController.authenticate()
        self.TorController.signal(Signal.NEWNYM)

    def _rotate_ip(self):
        attempts = 1
        new_ip = None
        while attempts <= 5:
            self._newCircuit()
            new_ip = self.check_ip()
            if new_ip == self.ip:
                attempts += 1
                if attempts != 6:
                    print("IP did not successfully rotate. Attempt {} ...".format(attempts))
                else:
                    print("Rotation failed. Better luck next time.")
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
        return requests.get("http://www.icanhazip.com").text[:-1]

    def get(self, url):
        page = requests.get(url)
        self._update_requests()
        if self._use_soup:
            return BeautifulSoup(page.content, 'html.parser')
        else:
            return page
