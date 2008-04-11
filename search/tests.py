r"""

>>> from models import Document
>>> from backends.simple import SimpleIndexer

>>> d = Document.objects.create(body=u"The Greatest Book Ever")
>>> d2 = Document.objects.create(body=u"Beginning Python")
>>> d3 = Document.objects.create(body=u"Python Network Programming")

The document contains a default ignore word.

>>> indexer = SimpleIndexer()
>>> indexer.make_words(d)
[<Word: greatest>, <Word: book>, <Word: ever>]

If a word has been used before it won't be re-created.

>>> words = indexer.make_words(d2)
>>> words
[<Word: beginning>, <Word: python>]
>>> more_words = indexer.make_words(d3)
>>> more_words
[<Word: python>, <Word: network>, <Word: programming>]
>>> words[1].pk == more_words[0].pk
True

"""