from datetime import datetime, timedelta

from django.conf import settings
from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sitemaps import ping_google

from managers import *
from applications.template_utils.markup import formatter
from applications.typogrify.templatetags.typogrify import typogrify


class Entry(models.Model):
    """
    """

    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3    
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
        
    # Dates
    published           = models.DateTimeField('Date Published', default=datetime.now)
    created             = models.DateTimeField(editable=False)
    updated             = models.DateTimeField(editable=False)
    
    # Meta
    author              = models.ForeignKey(User)
    title               = models.CharField(max_length=250, db_index=True)
    slug                = models.SlugField()
    
    # Content
    summary             = models.TextField(help_text='Enter a brief summary of this blog entry.')
    body                = models.TextField(help_text='Enter the main content of this entry.')
    footnotes           = models.TextField(blank=True, help_text='Enter footnotes if needed.')
    
    # Pre-Processed Content
    summary_processed   = models.TextField('Processed Summary', editable=False)
    body_processed      = models.TextField('Processed Body', editable=False)
    footnotes_processed = models.TextField('Processed Footnotes', blank=True, editable=False)
    
    # Options
    status              = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS, help_text='Select the status of this blog entry.')
    enable_comments     = models.BooleanField('Comments?', default=True, help_text='Select \'True\' if you wish to enable visitors to comment on this entry.')
    
    # Mangers
    objects             = models.Manager()
    live                = LiveEntryManager()
    
    class Meta:
        get_latest_by = 'published'
        ordering = ['-published']
        verbose_name_plural = 'entries'
    
    def __unicode__(self):
        return self.title
    
    @permalink
    def get_absolute_url(self):
        return ('entry-detail', (), {
            'year'  : self.published.year, 
            'month' : self.published.strftime('%b').lower(), 
            'day'   : self.published.day, 
            'slug'  : self.slug
        })
    
    def _next_previous_helper(self, direction):
        return getattr(self, 'get_%s_by_published' % direction)(status__exact=self.LIVE_STATUS)
    
    def _process_markup(self):
        """
        Returns the entry with content elements processed by markup and typogrify.
        """
        self.summary_processed = typogrify(formatter(self.summary))
        self.body_processed = typogrify(formatter(self.body))
        self.footnotes_processed = typogrify(formatter(self.footnotes))
        return self
    
    def get_comments(self):
        """
        Returns a list of comments associated with the entry.
        """
        from django.contrib.contenttypes.models import ContentType
        ctype = ContentType.objects.get(app_label__exact='blog', name__exact='entry')
        return Comment.objects.filter(content_type=ctype.id, object_id=self.id)
    
    def get_comment_count(self):
        """
        Returns the number of comments on the entry.
        """
        return self.get_comments().count()
    
    def get_featured_comments(self):
        """
        Returns a list of featured comments associated with the entry.
        """      
        return self.get_comments().filter(approved=True, is_featured=True)
    
    def get_featured_comment_count(self):
        """
        Returns the number of featured comments on the entry.
        """
        return self.get_featured_comments().count()
    
    def get_approved_comments(self):
        """
        Returns a list of approved comments associated with the entry.
        """            
        return self.get_comments().filter(approved=True)
    
    def get_approved_comment_count(self):
        """
        Returns the number of approved comments on the entry.
        """
        return self.get_approved_comments().count()
    
    def get_latest_comment(self):
        """
        Returns the latest comment on the entry.
        """
        return self.get_approved_comments().latest()
    
    def comment_period_open(self):
        """
        Returns True is comments are open on this entry (entry has been posted within the last 30 days).
        """
        return self.enable_comments and datetime.datetime.today() - datetime.timedelta(30) <= self.published
    
    @property
    def get_next(self):
        return self._next_previous_helper('next')
    
    @property
    def get_previous(self):
        return self._next_previous_helper('previous')
    
    def save(self):
        # Create or update the proper dates.
        if not self.id:
            self.created = datetime.now()
            self.updated = self.created
        else:
            self.updated = datetime.now()
        
        # Process markup language.
        self = self._process_markup()
        
        # Save this time, really.
        super(Entry, self).save()
        
        # Ping Google.
        try:
            ping_google()
        except Exception:
            pass
    

# Initialization
from blog import register
del register
