from OFS.Application import install_package
import plonesocial.auth.rpx
from plonesocial.auth.rpx.browser.rpx_view import PASInfoView
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import PloneSite
from Products.Five import zcml
from Products.Five import fiveconfigure
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

    def afterSetUp(self):
        # Since Zope 2.10.4 we need to install our package manually
        install_package(self.app, plonesocial.auth.rpx, plonesocial.auth.rpx.initialize)

    @property
    def pas(self):
        return self.portal.acl_users

    @property
    def pas_info(self):
        return PASInfoView(self.portal, None)
        #return self.pas.restrictedTraverse("@@pas_info")


class RPXFunctionalTestCase(PloneTestCase.Functional, RPXTestCase):
    pass
