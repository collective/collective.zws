# -*- coding: utf-8 -*-
###
# This module is a derivate of a work by Chris McDonough for Zope ClockServer.
#
# Copyright (c) 2005 Chris McDonough. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE
###

import os
import email
import time
import socket
import StringIO
import posixpath

from ZServer.medusa.http_server import http_request
from ZServer.medusa.default_handler import unquote
from ZServer.PubCore import handle
from ZServer.HTTPResponse import make_response
from ZPublisher.HTTPRequest import HTTPRequest

from zope.interface import implements

from collective.zws.interfaces import IWebSocketLayer
from asyncorews import websocket


class WebSocketServer(object):

    def __init__(self, port, host=None, logger=None, handler=None):
        h = self.headers = []
        h.append('User-Agent: WebSocket Server')
        h.append('Accept: text/html,text/plain')
        if host:
            h.append('Host: %s' % host)
        else:
            h.append('Host: %s' % socket.gethostname())

        if handler is None:
            handler = handle
        self.zhandler = handler

        self.server = websocket.WebSocketServer(
            port, handlers={'/.*': self.handler_factory}
        )

    def handler_factory(self, conn, path):
        return WebSocketHandler(self, conn, path)


class WebSocketRequest(HTTPRequest):
    implements(IWebSocketLayer)


class WebSocketChannel(object):
    """Medusa channel for WebSocket server
    """
    addr = ['127.0.0.1']
    closed = 0

    def __init__(self, server, conn):
        self.server = server
        self.conn = conn

    def push(self, producer, send=1):
        if type(producer) == str:
            lines = producer.split('\r\n')
            statusline = lines.pop(0)
            assert statusline
            message = email.message_from_string('\r\n'.join(lines))
            self.conn.send(unicode(message.get_payload(), 'utf-8'))

    def done(self):
        pass


class WebSocketHandler(object):

    # required by ZServer
    SERVER_IDENT = 'WebSocket'

    # request environment defaults
    _ENV = dict(REQUEST_METHOD='GET',
                SERVER_PORT='WebSocket',
                SERVER_NAME='WebSocket Server',
                SERVER_SOFTWARE='Zope',
                SERVER_PROTOCOL='HTTP/1.0',
                SCRIPT_NAME='',
                GATEWAY_INTERFACE='CGI/1.1',
                REMOTE_ADDR='0')

    def __init__(self, server, conn, method=None):
        self.server = server
        self.conn = conn
        self.method = method

    def get_requests_and_response(self, conn, data):
        out = StringIO.StringIO()
        s_req = '%s %s HTTP/%s' % ('GET', self.method, '1.0')
        req = http_request(WebSocketChannel(self, conn), s_req,
                           'GET', self.method,
                           '1.0', self.server.headers)
        env = self.get_env(req)
        resp = make_response(req, env)
        env['HTTP_COOKIE'] = conn.cookie
        env['WEBSOCKET_DATA'] = data
        return req, WebSocketRequest(out, env, resp), resp

    def get_env(self, req):
        env = self._ENV.copy()
        (path, params, query, fragment) = req.split_uri()
        if params:
            path = path + params  # undo medusa bug
        while path and path[0] == '/':
            path = path[1:]
        if '%' in path:
            path = unquote(path)
        if query:
            # ZPublisher doesn't want the leading '?'
            query = query[1:]

        env['PATH_INFO'] = '/' + path
        env['PATH_TRANSLATED'] = posixpath.normpath(
            posixpath.join(os.getcwd(), env['PATH_INFO']))
        if query:
            env['QUERY_STRING'] = query
        env['channel.creation_time'] = time.time()

        for header in req.header:
            key, value = header.split(':', 1)
            key = key.upper()
            value = value.strip()
            key = 'HTTP_%s' % ('_'.join(key.split('-')))
            if value:
                env[key] = value

        return env

    def dispatch(self, data):
        req, zreq, resp = self.get_requests_and_response(self.conn, data)
        self.server.zhandler('Zope2', zreq, resp)
