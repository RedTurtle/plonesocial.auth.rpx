from zope.interface import Interface
from plone.app.users.browser.register import RegistrationForm as BaseForm
from zope.component import getMultiAdapter
from zope.formlib import form
from zope import schema

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from plonesocial.auth.rpx import rpxMessageFactory


def get_email(self):
    rpx_view = getMultiAdapter((self.context, self.request), name='rpx_view')
    credentials = rpx_view.rpx_credentials
    return credentials.get('email')


def get_fullname(self):
    rpx_view = getMultiAdapter((self.context, self.request), name='rpx_view')
    credentials = rpx_view.rpx_credentials
    return credentials.get('displayName')


def get_username(self):
    rpx_view = getMultiAdapter((self.context, self.request), name='rpx_view')
    credentials = rpx_view.rpx_credentials
    return credentials.get('preferredUsername')


class IRPXRegisterSchema(Interface):

    telephone = schema.ASCIILine(
        title=rpxMessageFactory(u'label_rpx_telephone', default=u'Phone number'),
        description=rpxMessageFactory(u'help_rpx_telephone',
                      default=u"Enter your phone number"))

class RegistrationForm(BaseForm):
    """ Dynamically get fields from user data, through admin
        config settings.
    """

    @property
    def form_fields(self):
        defaultFields = super(RegistrationForm, self).form_fields
        if not defaultFields:
            return defaultFields
        defaultFields.get('email').get_rendered = get_email
        defaultFields.get('fullname').get_rendered = get_fullname
        defaultFields.get('username').get_rendered = get_username
        defaultFields = defaultFields.omit('rpx_identifier')
        return defaultFields + form.Fields(IRPXRegisterSchema)

    def getRPX(self):
        rpx_view = getMultiAdapter((self.context, self.request), name='rpx_view')
        return rpx_view.rpx_credentials.get('identifier')

    @form.action(_(u'label_register', default=u'Register'), validator='validate_registration', name=u'register')
    def action_join(self, action, data):
        ms_tool = getToolByName(self, 'portal_membership')
        self.handle_join_success(data)
        member = ms_tool.getMemberById(data['username'])
        rpx_ids = list(member.getProperty('rpx_identifier'))
        rpx_ids.append(self.getRPX())
        extra_properties = {}
        extra_properties['rpx_identifier'] = rpx_ids
        extra_properties['telephone'] = data.pop('telephone')
        member.setMemberProperties(extra_properties)
        if rpx_ids:
            return self.context.unrestrictedTraverse('rpx_registered')()
        else:
            return self.context.unrestrictedTraverse('registered')()

    def handle_join_success(self, data):
        registration = getToolByName(self.context, 'portal_registration')
        credentials = self.getRPX()
        if credentials:
            data['rpx_identifier'] = (credentials,)
            data['password'] = registration.generatePassword()
        return super(RegistrationForm, self).handle_join_success(data)
