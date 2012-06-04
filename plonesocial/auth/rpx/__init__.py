import install

install.register_rpx_plugin()

from zope.i18nmessageid import MessageFactory
rpxMessageFactory = MessageFactory('plonesocial.auth.rpx')


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    install.register_rpx_plugin_class(context)
