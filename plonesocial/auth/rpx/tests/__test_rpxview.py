import unittest
from plonesocial.auth.rpx.tests.base import RPXTestCase
from Products.PluggableAuthService.interfaces.plugins \
        import IExtractionPlugin, ILoginPasswordExtractionPlugin


class TestRPXView(RPXTestCase):
    def test_DefaultConfig(self):
        pas_info=self.pas_info
        self.assertEquals(pas_info.hasRPXExtractor(), False)
        self.assertEquals(pas_info.hasLoginPasswordExtractor(), True)

    def test_RPXInstalled(self):
        self.portal.portal_quickinstaller.installProduct("plonesocial.auth.rpx")
        pas_info=self.pas_info
        self.assertEquals(pas_info.hasRPXExtractor(), True)
        self.assertEquals(pas_info.hasLoginPasswordExtractor(), True)

    def testOnlyRPXInstalled(self):
        plugins=self.pas.plugins.listPlugins(IExtractionPlugin)
        for (id, plugin) in plugins:
            if ILoginPasswordExtractionPlugin.providedBy(plugin):
                plugin.manage_activateInterfaces(interfaces=())
        self.portal.portal_quickinstaller.installProduct("plonesocial.auth.rpx")

        pas_info=self.pas_info
        self.assertEquals(pas_info.hasRPXExtractor(), True)
        self.assertEquals(pas_info.hasLoginPasswordExtractor(), False)


def test_suite():
    suite=unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestRPXView))
    return suite


