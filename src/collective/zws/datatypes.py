# -*- coding: utf-8 -*-
import asyncore
import Lifetime


def lifetime_loop():
    # The main loop. Stay in here until we need to shutdown
    map = asyncore.socket_map
    timeout = 1.0
    while map and Lifetime._shutdown_phase == 0:
        asyncore.poll(timeout, map)


class WebSocketServerFactory(object):

    def __init__(self, section):
        self.port = section.port
        self.hostheader = section.host
        self.host = None  # appease configuration machinery

        # Override lifetime_loop for shorter asyncore loop poll timeout
        Lifetime.lifetime_loop = lifetime_loop

    def prepare(self, defaulthost='', dnsresolver=None,
                module=None, env=None, portbase=None):
        return

    def servertype(self):
        return "WebSocket Server"

    def create(self):
        from collective.zws.server import WebSocketServer
        from ZServer.AccessLogger import access_logger
        return WebSocketServer(self.port, self.hostheader, access_logger)
