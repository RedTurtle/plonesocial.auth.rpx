from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from plonesocial.auth.rpx.config import RPX_PROVIDERS


class ProvidersVocabulary(object):
    """Vocabulary factory for RPX providers."""

    implements(IVocabularyFactory)

    def __call__(self, context):
        items = RPX_PROVIDERS
        items_list = [Provider(item_id) for item_id in RPX_PROVIDERS.keys()]
        terms = [SimpleTerm(p.id, title=p.icon_tag_title) for p in items_list]
        return SimpleVocabulary(terms)

ProvidersVocabularyFactory = ProvidersVocabulary()


class Provider(object):
    """ represents a provider """#
    
    def __init__(self, id):
        self.id = id
        self.title = RPX_PROVIDERS[self.id]
        self.icon_tag = u"<img src='++resource++plonesocial.auth.rpx.icons/%s.png' title='%s' alt='%s'>" % (self.id, self.title, self.title)
        self.icon_tag_title = u"%s %s" % (self.icon_tag, self.title)


