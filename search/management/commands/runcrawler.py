
from django.conf import settings
from django.core.management import BaseCommand
from django.core.exceptions import ImproperlyConfigured

class Command(BaseCommand):
    
    def load_crawlers(self, indexer):
        crawlers = []
        for crawler_path in settings.SEARCH_CRAWLERS:
            try:
                dot = crawler_path.rindex(".")
            except ValueError:
                raise ImproperlyConfigured, "%s isn't a crawler module" % crawler_path
            crawler_module, crawler_classname = crawler_path[:dot], crawler_path[dot+1:]
            try:
                mod = __import__(crawler_module, {}, {}, [""])
            except ImportError, e:
                raise ImproperlyConfigured, 'Error importing middleware %s: "%s"' % (crawler_module, e)
            try:
                crawler_class = getattr(mod, crawler_classname)
            except AttributeError:
                raise ImproperlyConfigured, 'Middleware module "%s" does not define a "%s" class' % (crawler_module, crawler_classname)
            crawlers.append(crawler_class(indexer))
        return crawlers
    
    def handle(self, *args, **options):
        from search.backends.simple import SimpleIndexer
        crawlers = self.load_crawlers(SimpleIndexer())
        for crawler in crawlers:
            crawler.crawl()
