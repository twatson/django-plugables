from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from models import Entry


# Get the current site.
site = Site.objects.get_current()

class LatestEntries(Feed):
    """ 
    A feed of the latest blog entries.
    """
    
    title = '%s: the blog' % site.name
    link = 'http://%s/blog/' % site.domain
    
    def items(self):
        return Entry.live.all()[:25]
    
    def item_pubdate(self, item):
        return item.published
    
    def item_author_name(self, item):
        return item.author.get_full_name()
        
    item_author_email = ''
    
    def item_author_link(self, item):
        return '%s' % site.domain
    
