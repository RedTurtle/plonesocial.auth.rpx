## Controller Python Script "personalize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=visible_ids=None, portrait=None, listed=None, REQUEST=None, ext_editor=None
##title=Personalization Handler.

from Products.CMFPlone.utils import transaction_note
from Products.CMFPlone import PloneMessageFactory as _

member=context.portal_membership.getAuthenticatedMember()
member.setProperties(properties=context.REQUEST, REQUEST=REQUEST)
member_context=context.portal_membership.getHomeFolder(member.getId())
context.portal_skins.updateSkinCookie()

if member_context is None:
    member_context=context.portal_url.getPortalObject()

if visible_ids is None and REQUEST is not None:
    visible_ids=0
else:
    visible_ids=1
REQUEST.set('visible_ids', visible_ids)

if listed is None and REQUEST is not None:
    listed=0
else:
    listed=1
REQUEST.set('listed', listed)

if ext_editor is None and REQUEST is not None:
    ext_editor=0
else:
    ext_editor=1
REQUEST.set('ext_editor', ext_editor)

if (portrait and portrait.filename):
    context.portal_membership.changeMemberPortrait(portrait)

delete_portrait = context.REQUEST.get('delete_portrait', None)
if delete_portrait:
    context.portal_membership.deletePersonalPortrait(member.getId())


# RPX
rpx_view = context.restrictedTraverse('@@rpx_view')
delete_rpx_ids = REQUEST.get('delte_rpx_id', None)
new_rpx_provider = REQUEST.get('new_rpx_provider', None)
new_rpx_id = REQUEST.get('new_rpx_identifier', None)
if delete_rpx_ids:
    rpx_view.delete_rpx_id_from_member(member.getId(), delete_rpx_ids)
if new_rpx_id:
    rpx_view.add_rpx_id_to_member(member.getId(), new_rpx_provider, new_rpx_id)
    # remove new id from request
    #del REQUEST['new_rpx_identifier']
    #raise Exception, dir(REQUEST)
    REQUEST.set('new_rpx_identifier', None)



member.setProperties(listed=listed, ext_editor=ext_editor, visible_ids=visible_ids)

tmsg='Edited personal settings for %s' % member.getId()
transaction_note(tmsg)

context.plone_utils.addPortalMessage(_(u'Your personal settings have been saved.'))
return state
