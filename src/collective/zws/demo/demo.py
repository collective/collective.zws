# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView


class Echo(BrowserView):

    def __call__(self):
        return self.request.environ.get('WEBSOCKET_DATA')


class WhoAmI(BrowserView):

    def __call__(self):
        user_id = 'Anonymous User'
        mtool = getToolByName(self.context, 'portal_membership')
        if not mtool.isAnonymousUser():
            user_id = mtool.getAuthenticatedMember().getId()
        return user_id
