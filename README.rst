collective.zws
==============

Experimental (asyncore) WebSocket server integration for Zope2. Server is
started within the same asyncore loop with Zope2 (and Plone) and each websocket
request is handled via ZPublisher similarly to regular HTTP-requests (within
normal request/transaction environment, cookie based authentication etc..).

WebSocket-services are regular browser views registered for special
``collective.zws.interfaces.IWebSocketLayer``-layer. Only WebSocket-request
should implemetn that layer.

Trying out
----------

1. Buildout and start Plone::

    $ python bootstrap.py
    $ bin/buildout
    $ bin/instance fg

2. Create a Plone-site, e.g. Plone

3. Open http://localhost:8080/Plone/@@websocket-demo

Asyncore-based websocket-server is forked from (license is still unclear):
http://www.cs.rpi.edu/~goldsd/docs/spring2012-csci4220/websocket-py.txt

Tested to work with Firefox and Chrome. Unresolved handshaking issues
with Safari.

Todo
----

- Provide ZMQ-based pub/sub-example for sending data from zope.events
  to WebSocket-clients.

Limitations
-----------

This approach may never be scalable or otherwise suitable for enterprise
Plone-deployments (with ZEO, load balancing and everything). Use c.xmpp or
c.zamqp (with RabbitMQ web-stomp -plugin) there.
AMQP or 

