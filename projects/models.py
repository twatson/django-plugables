from django.db import models

from core.models import Item
from tagging.fields import TagField


class Project(models.Model):
    """
    A project is a wrapper around a code repository, connecting authors and
    other descriptive information to it.
    """
    
    name = models.CharField(max_length=100)
    description = models.TextField(help_text='A short description of the project.')
    repository = models.ForeignKey('CodeRepository', related_name='repository')
    maintainers = models.ManyToManyField('Maintainer', related_name='maintainer')
    slug = models.SlugField(unique=True)
    url = models.URLField(verify_exists=True, help_text='The URL to the project, usually hosted at Google Code.')
    tags = TagField()
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ('project-detail', (), {
            'slug': self.slug
        })
    

class Maintainer(models.Model):
    """
    A maintainer is a person with commmit rights to a given code repository.
    All this model contains is simple metadata, if available.
    """
    
    # Basics
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200)
    suffix = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    
    # URLs
    personal_url = models.URLField(blank=True, verify_exists=True)
    professional_url = models.URLField(blank=True, verify_exists=True)
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    def __unicode__(self):
        return self.name
        
    @permalink
    def get_absolute_url(self):
        return ('maintainer-detail', (), {
            'slug': self.slug
        })
    
    @property
    def name(self):
        if self.first_name or self.last_name:
            return ' '.join(b for b in (self.first_name, self.last_name) if b)
    
    @property
    def full_name(self):
        return ' '.join(b for b in (self.first_name, self.middle_name, self.last_name, self.suffix) if b)
    
    def get_projects(self):
        """
        Returns a string of projects for use in the admin list display.
        """
        
        maintainers = Project.objects.filter(maintainers=self)
        projects = []
        for maintainer in maintainers:
            projects.append(str(project.name))
        return ', '.join(projects)
    

class CodeRepository(models.Model):
    """
    A code repository that you check code into somewhere. Currently only SVN
    is supported, but other forms should be hard to support.
    """
    
    SCM_CHOICES = (
        ('svn', 'Subversion'),
    )
    
    type = models.CharField(max_length=3, choices=SCM_CHOICES, default='svn')
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    username = models.CharField(max_length=100, help_text='The maintainer\'s username for this SCR.')
    public_changeset_template = models.URLField(verify_exists=False, blank=True, help_text='Template for viewing a changeset publically. Use \'%s\' for the revision number')
    url = models.URLField(verify_exists=True)
    
    class Meta:
        verbose_name_plural = 'code repositories'
    
    def __unicode__(self):
        return self.name
    
    @permalink
    def get_absolute_url(self):
        return ('repository-detail', (), {
            'slug': self.slug
        })
    
    def updated(self):
        commits = CodeCommit.objects.filter('-committed')[:0]
        last_commit = commits.committed
        return last_commit
    

class CodeCommit(models.Model):
    """
    A code change that's been checked in.
    """
    
    repository = models.ForeignKey(CodeRepository, related_name='commits')
    revision = models.PositiveSmallIntegerField()
    message = models.TextField()
    committed = models.DateTimeField()
    
    class Meta:
        ordering = ['-revision']
    
    def __unicode__(self):
        return "[%s] %s" % (self.revision, text.truncate_words(self.message, 10))
        
    @property
    def url(self):
        if self.repository.public_changeset_template:
            return self.repository.public_changeset_template % self.revision
        return ""
    

# Initilization
from projects import register
del register

# Register item objects to be "followed"
Item.objects.follow_model(CodeCommit)