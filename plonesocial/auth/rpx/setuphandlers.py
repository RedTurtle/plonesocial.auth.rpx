from zope.component import getUtility
from zope.component import getMultiAdapter
from StringIO import StringIO
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from Products.CMFCore.utils import getToolByName

from plonesocial.auth.rpx.browser.rpx_view import PASInfoView
#from Products.PlonePAS.browser.info import PASInfoView
from plonesocial.auth.rpx.portlets.rpxportlet import Assignment as LoginAssignment



def hasRPXPlugin(portal):
    pas_info=PASInfoView(portal, None)
    return pas_info.hasRPXExtractor()


def createRPXPlugin(portal, out):
    print >>out, "Adding an RPX plugin"
    acl=getToolByName(portal, "acl_users")
    #acl.manage_addProduct["plonesocial.auth.rpx"].manage_add_rpx_helper(
    acl.manage_addProduct["plonesocial.auth.rpx"].manage_add_rpx_helper(
            id="rpx", title="RPX authentication plugin")


def activatePlugin(portal, out, plugin):
    acl=getToolByName(portal, "acl_users")
    plugin=getattr(acl, plugin)
    interfaces=plugin.listInterfaces()

    activate=[]

    for info in acl.plugins.listPluginTypeInfo():
        interface=info["interface"]
        interface_name=info["id"]
        if plugin.testImplements(interface):
            activate.append(interface_name)
            print >>out, "Activating interface %s for plugin %s" % \
                    (interface_name, info["title"])

    plugin.manage_activateInterfaces(activate)


def addLoginPortlet(portal, out):
    leftColumn = getUtility(IPortletManager, name=u'plone.leftcolumn', context=portal)
    left = getMultiAdapter((portal, leftColumn,), IPortletAssignmentMapping, context=portal)
    if u'rpx-login' not in left:
        print >>out, "Adding RPX login portlet to the left column"
        left[u'rpx-login'] = LoginAssignment()


def importVarious(context):
    # Only run step if a flag file is present (e.g. not an extension profile)
    if context.readDataFile('rpx-pas.txt') is None:
        return

    site = context.getSite()
    out = StringIO()
    #setup_configlet(site)
    if not hasRPXPlugin(site):
        createRPXPlugin(site, out)
        activatePlugin(site, out, "rpx")

    addLoginPortlet(site, out)

