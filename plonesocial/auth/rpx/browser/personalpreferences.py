
from zope.component import getUtility
from zope.formlib import form

from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.browser.account import AccountPanelSchemaAdapter
from plone.app.users.browser.personalpreferences import UserDataPanel

from Products.CMFDefault.formlib.widgets import FileUploadWidget
from Products.CMFPlone.utils import safe_unicode

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plonesocial.auth.rpx.browser.userdataschema import IRPXUserDataSchemaProvider


class RPXUserDataPanelAdapter(AccountPanelSchemaAdapter):

    def _getProperty(self, name):
        """ PlonePAS encodes all unicode coming from PropertySheets.
            Decode before sending to formlib. """
        value = self.context.getProperty(name, '')
        if value:
            return safe_unicode(value)
        return value

    def get_telephone(self):
        return self._getProperty('telephone')

    def set_telephone(self, value):
        if value is None:
            value = ''
        return self.context.setMemberProperties({'telephone': value})

    telephone = property(get_telephone, set_telephone)

class RPXUserDataPanel(UserDataPanel):

    def __init__(self, context, request):
        """ Load the UserDataSchema at view time.

        (Because doing getUtility for IUserDataSchemaProvider fails at startup
        time.)
        """
        super(UserDataPanel, self).__init__(context, request)
        util = getUtility(IUserDataSchemaProvider)
        base_schema = util.getSchema()
        base_field = form.FormFields(base_schema)
        rpx_util = getUtility(IRPXUserDataSchemaProvider)
        rpx_schema = rpx_util.getSchema()
        rpx_field = form.FormFields(rpx_schema)
        #make field in right order
        self.form_fields =  base_field.select('fullname') + \
                            base_field.select('email') + \
                            rpx_field + \
                            base_field.omit('email').omit('fullname')
        #import pdb; pdb.set_trace()
        self.form_fields['portrait'].custom_widget = FileUploadWidget

class RPXUserDataConfiglet(RPXUserDataPanel):
    """ """
    template = ViewPageTemplateFile('account-configlet.pt')
