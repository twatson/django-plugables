
from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Document(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    object = generic.GenericForeignKey()
    body = models.TextField()
    
    def __unicode__(self):
        return unicode(self.object)

class Word(models.Model):
    string = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.string

class WordPosition(models.Model):
    document = models.ForeignKey(Document, related_name="words")
    word = models.ForeignKey(Word, related_name="locations")
    position = models.PositiveIntegerField()
