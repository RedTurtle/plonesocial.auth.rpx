from plonesocial.auth.rpx.tests.rpxtestcase import FunctionalRPXTestCase
from zExceptions import Redirect
from zope.component import getMultiAdapter
from zope.publisher.browser import TestRequest


class TestRPXExtraction(FunctionalRPXTestCase):

    def test_empty_extraction(self):
        """Test if we do not invent credentials out of thin air.
        """
        creds=self.pas.rpx.extractCredentials(self.app.REQUEST)
        self.assertEqual(creds, {})

    def test_unique_rpx_id(self):
        """Test if a rpx id is not already mapped to an existing user
           when adding a User
        """
        session = self.app.session_data_manager.getSessionData()
        creds = {'identifier' : self.identity }
        self.set_credentials_to_session(creds)
        username1 = 'new_user'
        self.create_plone_user(login=username1)
        # assign creds to user
        rpx_view = getMultiAdapter((self.folder, TestRequest()), name='rpx_view')
        rpx_view.set_identifier_to_member(username1)

        ms = self.folder.portal_membership
        member = ms.getMemberById(username1)
        print 'rpx id: %s' % member.getProperty('rpx_identifier')




        import pdb;pdb.set_trace()


def test_suite():
    from unittest import TestSuite, makeSuite
    suite=TestSuite()
    suite.addTest(makeSuite(TestRPXExtraction))
    return suite
