import urllib
import urlparse
from zope.interface import implements, Interface
from zope.component import queryUtility
from plone.memoize.instance import memoize
from plone.app.controlpanel.security import ISecuritySchema
from Acquisition import aq_inner

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces import IPropertiesTool
from Products.PlonePAS.interfaces.browser import IPASInfoView
from Products.PluggableAuthService.interfaces.plugins \
                import IExtractionPlugin, ILoginPasswordExtractionPlugin


from plonesocial.auth.rpx.providers import Provider


class PASInfoView(BrowserView):
    implements(IPASInfoView)

    def checkExtractorForInterface(self, interface):
        acl = getToolByName(aq_inner(self.context), "acl_users")
        plugins=acl.plugins.listPlugins(IExtractionPlugin)
        for plugin in plugins:
            if interface.providedBy(plugin[1]):
                return True
        return False

    @memoize
    def hasLoginPasswordExtractor(self):
        return self.checkExtractorForInterface(ILoginPasswordExtractionPlugin)

    @memoize
    def hasRPXExtractor(self):
        try:
            from plonesocial.auth.rpx.interface import IRPXExtractionPlugin
        except ImportError:
            return False
        return self.checkExtractorForInterface(IRPXExtractionPlugin)



class IRPXView(Interface):
    """
    rpx view interface
    """

    def rpx_credentials():
        """return credentials returned by rpx"""

    def set_identifier_to_member(member_id):
        """ set user's rpx identifier """

    def self_register_enabled(self):
        """ return the enable_self_reg setting from plone_control_panel/security """

    def rpx_identifier_is_unique():
        """ check if rpx id has not been added to a different user before """

    def delete_rpx_id_from_member(member_id, rpx_id):
        """ delete rpx ids from the specified user """

    def add_rpx_id_to_member(member_id, rpx_provider, rpx_id):
        """ adds a new rpx identifier to specified user """

    def rpx_providers(self):
        """ return a list of possible rpx providers """



class RPXView(BrowserView):
    """
    rpx browser view
    """
    implements(IRPXView)

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.props = getattr(queryUtility(IPropertiesTool), 'rpx_properties', None)

    @property
    def portal_catalog(self):
        return getToolByName(self.context, 'portal_catalog')

    @property
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def portal(self):
        return getToolByName(self.context, 'portal_url').getPortalObject()

    @property
    def lang(self):
        pl = getToolByName(self.context, 'portal_languages')
        return pl.getPreferredLanguage()[:2]
    
    @property
    def rpx_is_configured(self):
        return self.domain and self.props.getProperty("api_key")

    @property
    def domain(self):
        return self.props.getProperty("domain")

    @property
    def popup_url(self):
        return urlparse.urljoin(self.domain,"openid/v2/signin")

    @property
    def embed_url(self):
        return urlparse.urljoin(self.domain,"openid/embed")

    @property
    def rpx_token_url(self):
        return u'%s/rpx_callback' % self.portal.absolute_url()

    @property
    def providers(self):
        return [Provider(pid) for pid in self.props.getProperty('providers', [])]

    @property
    def rpx_credentials(self):
        session = self.context.session_data_manager.getSessionData(0)
        if session is not None:
            creds = session.get('rpx_credentials', {})
            return creds
        return {}

    @property
    def self_register_enabled(self):
        return ISecuritySchema(self.portal).enable_self_reg

    @property
    def rpx_identifier_is_unique(self):
        for member in self.portal_membership.listMembers():
            member_rpx_id = member.getProperty('rpx_identifier')
            rpx_identifier = self.rpx_credentials.get('identifier')
            if rpx_identifier in member_rpx_id:
                return False
        return True

    def token_url(self, came_from=None):
        if came_from is None:
            came_from = self.context.absolute_url()
        return '%s?came_from=%s' % (urllib.quote(self.rpx_token_url), came_from)

    def set_identifier_to_member(self, member_id):
        if self.rpx_credentials:
            member = self.portal_membership.getMemberById(member_id)
            rpx_ids = list(member.getProperty('rpx_identifier'))
            rpx_ids.append(self.rpx_credentials.get('identifier'))
            member.setProperties(rpx_identifier=rpx_ids)

    def add_rpx_id_to_member(self, member_id, rpx_provider, rpx_id):
        member = self.portal_membership.getMemberById(member_id)
        rpx_ids = list(member.getProperty('rpx_identifier'))
        rpx_ids.append(rpx_id)
        member.setProperties(rpx_identifier=rpx_ids)

    def delete_rpx_id_from_member(self, member_id, delete_rpx_ids):
        if delete_rpx_ids.__class__.__name__ not in ['tuple', 'list']:
            delete_rpx_ids = (delete_rpx_ids, )
        member = self.portal_membership.getMemberById(member_id)
        member_rpx_ids = list(member.getProperty('rpx_identifier'))
        for rpx_id in delete_rpx_ids:
            if rpx_id in delete_rpx_ids:
                member_rpx_ids.remove(rpx_id)
        member.setProperties(rpx_identifier=member_rpx_ids)
