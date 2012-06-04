import urllib
import urllib2
from simplejson import loads

from Acquisition import aq_parent
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin, IExtractionPlugin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IPropertiesTool
from zope.component import getUtility
import logging

from plonesocial.auth.rpx.config import RPX_AUTH_INFO_URL

logger = logging.getLogger("plonesocial.auth.rpx")

class RPXPlugin(BasePlugin):
    """ Map credentials to a user ID.
    """
    security = ClassSecurityInfo()

    def __init__( self, id, title=None ):
        self._setId( id )
        self.title = title

    def portal_url(self):
        pas=self._getPAS()
        site=aq_parent(pas)
        return site.absolute_url()

    def get_credentials_from_rpx(self, token):
        properties = getattr(getUtility(IPropertiesTool), 'rpx_properties', None)
        api_params = {
                    'token': token,
                    'apiKey': properties.api_key,
                    'format': 'json',
                    }
        http_response = urllib2.urlopen(RPX_AUTH_INFO_URL, urllib.urlencode(api_params))
        auth_info_json = http_response.read()
        auth_info = loads(auth_info_json)
        if auth_info['stat'] == 'ok':
            return  auth_info['profile'].copy()
        elif auth_info['stat'] == 'fail':
            logger.error("RPX credentials extraction failed: %s" % auth_info['err']['msg'])
        return {}

    # IExtractionPlugin implementation
    def extractCredentials(self, request):
        """This method performs the PAS credential extraction.
        """
        token = request.form.get('token', None)
        creds = {}
        if token is not None:
            session = self.session_data_manager.getSessionData()
            creds = self.get_credentials_from_rpx(token)
            session['rpx_credentials'] = creds
        return creds


    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):

        """ credentials -> (userid, login)

        o 'credentials' will be a mapping, as returned by IExtractionPlugin.

        o Return a  tuple consisting of user ID (which may be different
          from the login name) and login

        o If the credentials cannot be authenticated, return None.
        """
        rpx_identifier = credentials.get('identifier')
        if rpx_identifier is not None:
            ms_tool = getToolByName(self, 'portal_membership')
            user_id = login = ''
            for member in ms_tool.listMembers():
                member_rpx_id = member.getProperty('rpx_identifier')
                if rpx_identifier in member_rpx_id:
                    user_id = login = member.getId()
                    break
            if user_id and login:
                self._getPAS().updateCredentials(self.REQUEST,
                            self.REQUEST.RESPONSE, login, "")
                return (user_id, login)
            else:
                logger.error("RPX authentication failed for %s" % login)
        return None


classImplements(RPXPlugin, IAuthenticationPlugin, IExtractionPlugin)
