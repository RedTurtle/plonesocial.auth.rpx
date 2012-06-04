import urllib2
import urllib

from zope.component import getMultiAdapter
from OFS.Application import install_package
#from plone.session.tests.sessioncase import PloneSessionTestCase
from Testing.ZopeTestCase.placeless import setUp, tearDown
from Testing.ZopeTestCase.placeless import zcml
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite
from Products.Five import zcml, fiveconfigure
from Products.CMFCore.utils import getToolByName
from Testing.makerequest import makerequest
from Products.Archetypes.tests.utils import DummySessionDataManager

import plonesocial.auth.rpx
from plonesocial.auth.rpx.plugin import RpxHelper
from plonesocial.auth.rpx.browser.rpx_view import PASInfoView

from plonesocial.auth.rpx.config import RPX_POPUP_URL

PloneTestCase.setupPloneSite()

class RPXTestCase(PloneTestCase.PloneTestCase):

    class layer(PloneSite):
        @classmethod
        def setUp(cls):
            fiveconfigure.debug_mode = True
            zcml.load_config('configure.zcml',
                             plonesocial.auth.rpx)
            fiveconfigure.debug_mode = False

        @classmethod
        def tearDown(cls):
            pass

    identity = "fake_rpx_identity"

    session = {}

    server_response = {
                'preferredUsername'        : '',
                'displayName'              : '',
                'name'                     : {
                                              'givenName'  : '',
                                              'formatted'  : '',
                                              'familyName' : ''
                                              },
                'providerName'             : '',
                'address'                  : {
                                              'country'    : ''
                                              },
                'verifiedEmail'            : '',
                'identifier'               : '',
                'email'                    : ''
    }

    def afterSetUp(self):
        PloneTestCase.PloneTestCase.afterSetUp(self)
        install_package(self.app, plonesocial.auth.rpx, plonesocial.auth.rpx.initialize)
        self.acl_users = self.portal.acl_users
        self.portal.portal_quickinstaller.installProduct("plonesocial.auth.rpx")

        portal_properties = getToolByName(self.portal, 'portal_properties')
        self.props = portal_properties.site_properties

        # sessioning setup
        if 'session_data_manager' in self.app.objectIds():
            self.app._delObject('session_data_manager')
        self.app._setObject('session_data_manager', DummySessionDataManager())

    @property
    def request(self):
        return {}

    @property
    def portal_membership(self):
        return getToolByName(self.portal, 'portal_membership')

    @property
    def pas(self):
        return self.portal.acl_users

    @property
    def pas_info(self):
        return PASInfoView(self.portal, None)

    def create_plone_user(self, login="new_user", password="secret",
                          roles=[], groups=[], domains=()):
        self.acl_users.userFolderAddUser(
            login,
            password,
            roles = roles,
            groups = groups,
            domains = domains,
            )

    def set_credentials_to_session(self, creds={}):
        session = self.app.session_data_manager.getSessionData()
        session['rpx_credentials'] = creds

    def add_rpx_id_to_user(self, username="new_user"):
        member = self.portal_membership.getMemberById("new_user")
        member.setProperties(rpx_identifier=list(self.identity))
        self.props.manage_changeProperties(rpx_identifier=list(self.identity))

    def get_token_from_rpx(self):
        """ make a call to rpx an and get back token"""
        url_params = {'token_url' : ''}
        http_response = urllib2.urlopen(RPX_POPUP_URL, urllib.urlencode(url_params))
        import pdb;pdb.set_trace()




class FunctionalRPXTestCase(PloneTestCase.Functional, RPXTestCase):
    pass
