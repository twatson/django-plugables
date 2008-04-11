
import lucene as PyLucene

from search import Indexer

class LuceneIndexer(Indexer):
    
    def __init__(self, path):
        self.path = path
        super(LuceneIndexer, self).__init__()
        self.store = self.create_store()
        self.writer = self.create_writer()
    
    def create_store(self):
        return PyLucene.FSDirectory.getDirectory(self.path, True)
    
    def create_writer(self):
        writer = PyLucene.IndexWriter.open(self.store, PyLucene.StandAnalyzer(), True)
        writer.setMaxFieldLength(1048576)
        return writer
    
    def add(self, document):
        pass
