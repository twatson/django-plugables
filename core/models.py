from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey

from managers import ItemManager
from tagging.fields import TagField


class Item(models.Model):
    """
    A generic item used to tie the objects to the respective data provider.
    """
    
    # Generic relation to the object.
    content_type = models.ForeignKey(ContentType)
    object_id = models.IntegerField()
    object = GenericForeignKey()
    
    # "Standard" metadata each object provides.
    url = models.URLField(blank=True)
    timestamp = models.DateTimeField()
    tags = TagField()
    
    # Metadata about where the object "came from" -- used by data providers to
    # figure out which objects to update when asked.
    source = models.CharField(max_length=100, blank=True)
    source_id = models.TextField(blank=True)
    
    # Denormalized object __str__, for performance 
    object_str = models.TextField(blank=True)
    
    objects = ItemManager()
    
    class Meta:
        ordering = ['-timestamp']
        unique_together = [('content_type', 'object_id')]
    
    def __str__(self):
        return "%s: %s" % (self.content_type.model_class().__name__, self.object_str)
        
    def __cmp__(self, other):
        return cmp(self.timestamp, other.timestamp)
    
    def save(self):
        ct = '%s %s' % (self.content_type.app_label, self.content_type.model.lower())
        self.object_str = str(self.object)
        if hasattr(self.object, 'url'):
            self.url = self.object.url
        super(Item, self).save()
    

# Initilization
from core import register
del register
