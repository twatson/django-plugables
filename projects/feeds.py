from django.conf import settings
from django.contrib.syndication.feeds import Feed, FeedDoesNotExist
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType

from models import Project, CodeRepository, CodeCommit


# Get the current site.
site = Site.objects.get_current()

class LatestCommits(Feed):
    """ 
    A feed of the latest commits.
    """
    
    title = '%s: recent commits' % site.name
    link = 'http://%s/commits/' % site.domain
    
    def description(self):
        return 'The latest commits for all the projects on %s' % site.name
    
    def items(self):
        return CodeCommit.objects.all()[:50]
    
    def item_pubdate(self, item):
        return item.committed
    
    def item_link(self, item):
        if item.repository.public_changeset_template:
            return item.repository.public_changeset_template % item.revision
        else:
            return self.link
                
    item_author_name = ''
    
    item_author_email = ''
    

# class LatestCommitsByProject(Feed):
#     def get_object(self, bits):
#         if len(bits) != 1:
#             return CodeCommit.objects.all()[:50]
#         else:
#             return Project.objects.get(beat__exact=bits[0])
#     
#     def title(self, obj):
#         return "%s: latest commits for %s" % site.name, obj.beat
#     
#     def link(self, obj):
#         if not obj:
#             raise FeedDoesNotExist
#         return obj.get_absolute_url()
#     
#     def description(self, obj):
#         return "The latest commits for %s" % obj.beat
#     
#     def items(self, obj):
#         return Repository.objects.filter(project__id__exact=obj.id).order_by('-crime_date')[:30]