import unittest
from plonesocial.auth.rpx.tests.rpxtestcase import FunctionalRPXTestCase
from zExceptions import Redirect


class TestRPXAuthentication(FunctionalRPXTestCase):

    def buildServerResponse(self):
        credentials={}
        for field in self.server_response.keys():
            credentials[field]=field
        credentials["identifier"]=self.identity
        credentials["providerName"]="Google"
        # this isn't part of the server response, but is added to the
        # credentials by PAS
        credentials["extractor"] = "rpx"
        return credentials

    def testEmptyAuthentication(self):
        """Test if we do not invent an identity out of thin air.
        """
        creds=self.pas.rpx.authenticateCredentials({})
        self.assertEqual(creds, None)

    def test_map_user_to_rpxid(self):
        member_id = "new_user"
        self.create_plone_user(member_id)
        self.add_rpx_id_to_user(member_id)
        member = self.portal_membership.getMemberById(member_id)
        print "member_rpx_id: %s" % member.getProperty('rpx_identity')
        print "fake_rpx_id: %s" % self.identity
        self.assertTrue(self.identity in member.getProperty('rpx_identity'))

    #def testServerAuthentication(self):
    #    """Test authentication of RPX server responses.
    #    """
    #    credentials=self.buildServerResponse()
    #    creds=self.pas.rpx.authenticateCredentials(credentials)
    #    self.assertEqual(creds, (self.identity, self.identity))



def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(TestRPXAuthentication))
    return suite
