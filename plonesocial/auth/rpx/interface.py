from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin, IAuthenticationPlugin
from zope.interface import Interface
from zope import schema


class IRPXExtractionPlugin(IExtractionPlugin):
    """Extract RPX credential information from a request.
    """
    def initiateAuthentication(identity_url, return_to=None):
        """Initiate the RPX authentication.
        """
    def extractCredentials(request):
        """ extract credentials from rpx response
        """


class IRpxHelper(# -*- implemented plugins -*-
                    IAuthenticationPlugin,
                    IRPXExtractionPlugin,
                                ):
    """interface for RpxHelper."""

