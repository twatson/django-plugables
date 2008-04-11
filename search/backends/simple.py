
import re

from django.db import connection

from search import Indexer, Searcher
from search.models import Document, Word, WordPosition

DEFAULT_IGNORE_WORDS = ("a", "and", "in", "is", "it", "the", "to",)

class SimpleIndexer(Indexer):
    def __init__(self, ignore_words=None):
        self.ignore_words = ignore_words or DEFAULT_IGNORE_WORDS
    
    def make_words(self, document):
        split_word = re.compile("\\W*")
        words = []
        for word in split_word.split(document.body):
            # normalize word
            word = word.lower()
            if not word or word in self.ignore_words:
                continue
            words.append(Word.objects.get_or_create(string=word)[0])
        return words
        
    def add(self, document):
        words = self.make_words(document)
        for position, word in enumerate(words):
            document.words.add(WordPosition(word=word, position=position))

class SimpleSearcher(Searcher):
    
    def find_word_rows(self, words):
        sql = {"fields": "w0.document_id", "tables": "", "clauses": ""}
        word_objs, table_count = [], 0
        for word in words:
            try:
                word_obj = Word.objects.get(string=word)
            except Word.DoesNotExist:
                continue
            word_objs.append(word_obj)
            if table_count > 0:
                sql["tables"] += ", "
                sql["clauses"] += " AND "
                sql["clauses"] += "w%d.document_id = w%d.document_id AND " % (
                    table_count - 1, table_count)
            sql["fields"] += ", w%d.position" % table_count
            sql["tables"] += "search_wordposition w%d" % table_count
            sql["clauses"] += "w%d.word_id = %d" % (table_count, word_obj.pk)
            table_count += 1
        cursor = connection.cursor()
        query = "SELECT %(fields)s FROM %(tables)s WHERE %(clauses)s" % sql
        cursor.execute(query)
        rows = []
        for row in cursor.fetchall():
            rows.append(row)
        return rows, word_objs
    
    def calculate_scores(self, rows, words):
        document_scores = dict([(row[0], 0) for row in rows])
        weights = [
            (1.0, self.score_frequency(rows)),
            (1.0, self.score_position(rows)),
        ]
        for weight, scores in weights:
            for document_pk in document_scores:
                document_scores[document_pk] += weight * scores[document_pk]
        return document_scores
    
    def _normalize_scores(self, scores, small_is_better=False):
        """
        Due to the nature of some algorithms the scores need to be normalized.
        Some algorithms may represent small numbers as better while others will
        do the exact oposite. This function will normalize the scores to be
        within a 0 - 1 range taking in the small_is_better flag.
        """
        vs = 0.00001 # avoids division by zero
        if small_is_better:
            min_score = min(scores.values())
            return dict([(u, float(min_score) / max(vs, l)) for u, l in scores.items()])
        else:
            max_score = max(scores.values())
            if max_score == 0:
                max_score = vs
            return dict([(u, float(c) / max_score) for u, c in scores.items()])
    
    def score_frequency(self, rows):
        """
        Scores based on the frequency of the words.
        """
        counts = dict([(row[0], 0) for row in rows])
        for row in rows:
            counts[row[0]] += 1
        return self._normalize_scores(counts)
    
    def score_position(self, rows):
        """
        Scores based on the position of the words.
        """
        positions = dict([(row[0], 1000000) for row in rows])
        for row in rows:
            pos = sum(row[1:])
            if pos < positions[row[0]]:
                positions[row[0]] = pos
        return self._normalize_scores(positions, small_is_better=True)
    
    def query(self, q):
        hits = []
        words = q.split()
        scores = self.calculate_scores(*self.find_word_rows(words))
        ranked_scores = sorted([(score, document_pk) for document_pk, score in scores.items()])
        for score, document_pk in ranked_scores[:10]:
            document = Document.objects.get(pk=document_pk)
            hits.append((score, document.object))
        return hits
        