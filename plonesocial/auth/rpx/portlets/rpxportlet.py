from zope.interface import Interface
from zope.interface import implements

from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from zope import schema
from zope.formlib import form
from zope.component import getMultiAdapter
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


class IRPXPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    # TODO: Add any zope.schema fields here to capture portlet configuration
    # information. Alternatively, if there are no settings, leave this as an
    # empty interface - see also notes around the add form and edit form
    # below.

    # some_field = schema.TextLine(title=_(u"Some field"),
    #                              description=_(u"A field to use"),
    #                              required=True)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IRPXPortlet)

    # TODO: Set default values for the configurable parameters here

    # some_field = u""

    # TODO: Add keyword parameters for configurable parameters here
    # def __init__(self, some_field=u"):
    #    self.some_field = some_field

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return "RPX-Authentication portlet"


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('rpxportlet.pt')

    def show(self):
        if self.portal_membership.isAnonymousUser():
            return True
        return False
    
    def popup_js(self):
        return u"""
          RPXNOW.overlay = true;
          RPXNOW.language_preference = '%s';
          """ % self.rpx_view.lang

    @property
    @memoize
    def portal_membership(self):
        return getToolByName(self.context, 'portal_membership')

    @property
    def rpx_view(self):
        return getMultiAdapter((self.context, self.request), name='rpx_view')
    
    @property
    def rpx_is_configured(self):
        return self.rpx_view.rpx_is_configured

    @property
    def popup_url(self):
        return self.rpx_view.popup_url

    @property
    def token_url(self):
        return self.rpx_view.rpx_token_url
    
    @property
    def providers(self):
        return self.rpx_view.providers


# NOTE: If this portlet does not have any configurable parameters, you can
# inherit from NullAddForm and remove the form_fields variable.

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IRPXPortlet)

    def create(self, data):
        return Assignment(**data)

