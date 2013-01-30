from zope.interface import Interface, implements
from zope import schema
from plonesocial.auth.rpx import rpxMessageFactory


class IRPXUserDataSchemaProvider(Interface):
    """
    """

    def getSchema():
        """
        """


class RPXUserDataSchemaProvider(object):
    implements(IRPXUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IRPXUserDataSchema


class IRPXUserDataSchema(Interface):
    """
    """

    telephone = schema.ASCIILine(
        title=rpxMessageFactory(u'label_rpx_telephone', default=u'Phone number'),
        description=rpxMessageFactory(u'help_rpx_telephone',
                      default=u"Enter your phone number"),
        required=True)