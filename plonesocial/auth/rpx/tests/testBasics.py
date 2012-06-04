import unittest
from plonesocial.auth.rpx.tests.rpxtestcase import RPXTestCase


class BasicTestCase(RPXTestCase):

    def test_rpx_installed(self):
        pas_info=self.pas_info
        self.assertEquals(pas_info.hasRPXExtractor(), True)
        self.assertEquals(pas_info.hasLoginPasswordExtractor(), True)

    def test_add(self):
        self.create_plone_user('new_user', '123456')
        self.failUnless(self.acl_users.getUser("new_user"))



def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(BasicTestCase))
    return suite
