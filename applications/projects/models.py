from datetime import datetime

from django.db import models
from django.db.models import permalink
from django.utils import text

#from core.models import Item
from tagging.fields import TagField


class Developer(models.Model):
    """
    A maintainer is a person with commmit rights to a given code repository.
    All this model contains is simple metadata, if available.
    """
    
    # Basics
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200)
    suffix = models.CharField(max_length=100, blank=True)
    svn_name = models.CharField('SVN name', max_length=100, blank=True)
    slug = models.SlugField(unique=True)
    
    # URLs
    personal_url = models.URLField('personal URL', blank=True, verify_exists=True)
    professional_url = models.URLField('professional URL', blank=True, verify_exists=True)
    django_people_url = models.URLField('Django People Profile', blank=True, verify_exists=True)
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    def __unicode__(self):
        return '%s (%s)' % (self.name, self.svn_name)
    
    @permalink
    def get_absolute_url(self):
        return ('developer-detail', (), {
            'slug': self.slug
        })
    
    @property
    def name(self):
        if self.first_name or self.last_name:
            return ' '.join(b for b in (self.first_name, self.last_name) if b)
    
    @property
    def full_name(self):
        return ' '.join(b for b in (self.first_name, self.middle_name, self.last_name, self.suffix) if b)
    

class Committer(models.Model):
    """
    A class that creates a simple relationship between a person who commits
    code into a repository listed in the directory and a developer in the
    directory.
    """
    
    developer = models.ForeignKey(Developer, unique=True)
    committer_name = models.CharField(max_length=50)
    

class Project(models.Model):
    """
    A project is a wrapper around a code repository, connecting authors and
    other descriptive information to it.
    """
    
    name = models.CharField(max_length=100)
    tagline = models.CharField(max_length=250, help_text="A few words about the project.")
    description = models.TextField(blank=True, help_text='A short description of the project.')
    created = models.DateTimeField(editable=False)
    owners = models.ManyToManyField(Developer, related_name='owners', blank=True, null=True)
    members = models.ManyToManyField(Developer, related_name='members', blank=True, null=True)
    slug = models.SlugField(unique=True)
    url = models.URLField('project URL', verify_exists=True, help_text='The URL to the project, usually hosted at Google Code.')
    extra_urls = models.TextField('additional URLs')
    tags = TagField()
    active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ('project-detail', (), {
            'slug': self.slug
        })
        
    def save(self):
        if not self.id:
            self.created = datetime.now()
        
        # Save this time, really.
        super(Project, self).save()
    

class Repository(models.Model):
    """
    A code repository that you check code into somewhere. Currently only SVN
    is supported, but other forms should be hard to support.
    """
    
    SCM_CHOICES = (
        ('svn', 'Subversion'),
        ('git', 'Git'),
        ('mer', 'Mercurial'),
        ('baz', 'Bazar'),
    )
    
    project = models.ForeignKey(Project, related_name='repository')
    type = models.CharField(max_length=3, choices=SCM_CHOICES, default='svn')
    public_changeset_template = models.URLField(verify_exists=False, blank=True, help_text='Template for viewing a changeset publically. Use \'%s\' for the revision number')
    url = models.URLField('repository URL', verify_exists=False)
    
    class Meta:
        verbose_name_plural = 'code repositories'
    
    def __unicode__(self):
        return self.project.name
    
    def updated(self):
        commits = Changeset.objects.filter(repository=self.id)[0]
        last_commit = commits.committed
        return last_commit
    

class Changeset(models.Model):
    """
    A code change that's been checked in.
    """
    
    repository = models.ForeignKey(Repository, related_name='commits')
    committer = models.ForeignKey(Committer, related_name='committer')
    revision = models.PositiveSmallIntegerField()
    message = models.TextField()
    committed = models.DateTimeField()
    
    class Meta:
        ordering = ['-committed']
        get_latest_by = 'committed'
    
    def __unicode__(self):
        return "[%s] %s" % (self.revision, text.truncate_words(self.message, 10))
    
    @property
    def url(self):
        if self.repository.public_changeset_template:
            return self.repository.public_changeset_template % self.revision
        else:
            return ''
    

class Change(models.Model):
    """
    A ``Change`` is a subset of a ``Changeset`` that displays more information
    about the instance including files that were added, deleted or modified as
    well as the changes within files that were modified.
    """
    
    ADD = 1
    MODIFY = 2
    DELETE = 3
    TYPE_CHOICES = (
        (ADD, 'Add'),
        (MODIFY, 'Modify'),
        (DELETE, 'Delete'),
    )
    
    changeset = models.ForeignKey(Changeset, related_name='change')
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    path = models.TextField()
    diff = models.TextField()
    

# Initilization
from projects import register
del register

# Register item objects to be "followed"
#Item.objects.follow_model(Changeset)
