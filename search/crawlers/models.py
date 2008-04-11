
from django.db.models.loading import cache
from django.contrib.contenttypes.models import ContentType

from search import Crawler, registry
from search.models import Document

class ModelCrawler(Crawler):
    """
    Crawls Django models.
    """
    
    def crawl(self):
        if not registry:
            print "No models registered to index."
        for opts in registry.values():
            ct = ContentType.objects.get_for_model(opts.model)
            for instance in opts.manager.all():
                values = []
                document = Document(content_type=ct, object_id=instance.pk)
                for field in fields:
                    values.append(getattr(instance, field))
                document.body = "".join(values)
                document.save()
                self.indexer.add(document)
    