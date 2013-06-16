collective.zws
==============

Experimental (asyncore) WebSocket server integration for Zope2. Server is
started into the same asyncore loop with Zope2 (and Plone) and each websocket
request is handled via ZPublisher similarly to regular HTTP-requests.

1. ::

    $ python bootstrap.py
    $ bin/buildout

2. Create Plone-site named 'Plone'

3. Open http://localhost:8080/Plone/@@demo

Includes asyncore-based websocket-server from:
http://www.cs.rpi.edu/~goldsd/docs/spring2012-csci4220/websocket-py.txt

Tested to work with Firefox and Chrome but the used had issues with Safari.


