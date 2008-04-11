
__all__ = ("Crawler", "Indexer", "Searcher")

class Crawler(object):
    def __init__(self, indexer):
        self.indexer = indexer
    
    def crawl(self):
        raise NotImplemented()

class Indexer(object):
    def __init__(self):
        pass
    
    def add(self, data):
        """
        Adds data to the index.
        """
        raise NotImplemented()

class Searcher(object):
    """
    Backend specific searcher to scan the index and return hits.
    """
    def query(self, q):
        raise NotImplemented()
