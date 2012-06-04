from zope.interface import implements, Interface

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class IRPXCallback(Interface):
    """RPXCallback browser view interface"""


class RPXCallback(BrowserView):
    """
    RPXCallback browser view
    """
    implements(IRPXCallback)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if self.portal_membership.isAnonymousUser():
            session = self.context.session_data_manager.getSessionData()
            creds = session.get('rpx_credentials', {})
            if not creds:
                msg = u'RPX authentication has failed. Try again later. You can still register login with your Plone username.'
                util = self.context.plone_utils
                util.addPortalMessage(msg, 'error')
            self.request.RESPONSE.redirect('%s/rpx_login_form' % self.portal.absolute_url())
        else:
            url = self.request.get('came_from')
            if url is not None:
                self.request.RESPONSE.redirect(url)
            else:
                self.request.RESPONSE.redirect(self.portal.absolute_url())

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()
