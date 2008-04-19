from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.syndication.views import feed

from models import Project, Repository, Changeset, Developer
from feeds import LatestProjects, LatestCommits#, LatestCommitsByProject

# Feeds
feeds = {
    'projects': LatestProjects,
    'commits': LatestCommits,
}


# Querysets
project_list = {
    'queryset': Project.objects.select_related(),
    'template_object_name': 'project',
}

project_detail = {
    'queryset': Project.objects.select_related(),
    'template_object_name': 'project',
}

developer_list = {
    'queryset': Developer.objects.all(),
    'template_object_name': 'developer',
}

developer_detail = {
    'queryset': Developer.objects.all(),
    'template_object_name': 'developer',
}

repository_list = {
    'queryset': Repository.objects.all(),
    'template_object_name': 'repository',   
}

commit_list = {
    'queryset': Changeset.objects.all(),
    'template_object_name': 'commit',
    'paginate_by': 50,
}


# URL Patterns
urlpatterns = patterns('',

    # Projects
    url(
        regex   = '^projects/(?P<slug>[-\w]+)/$',
        view    = list_detail.object_detail,
        kwargs  = project_detail,
        name    = 'project-detail',
    ),
    url(
        regex   = '^projects/$',
        view    = list_detail.object_list,
        kwargs  = project_list,
        name    = 'project-list',
    ),
    
    # Developers
    url(
        regex   = '^developers/(?P<slug>[-\w]+)/$',
        view    = list_detail.object_detail,
        kwargs  = developer_detail,
        name    = 'developer-detail',
    ),
    url(
        regex   = '^developers/$',
        view    = list_detail.object_list,
        kwargs  = developer_list,
        name    = 'developer-list',
    ),
    
    # Repositories
    url(
        regex   = '^repositories/$',
        view    = list_detail.object_list,
        kwargs  = repository_list,
        name    = 'repository-list',
    ),
    url(
        regex   = '^commits/$',
        view    = list_detail.object_list,
        kwargs  = commit_list,
        name    = 'commit-list',
    ),
    
    # Homepage
    url(
        regex   = '^$',
        view    = direct_to_template,
        kwargs  = { 'template': 'home.html' },
        name    = 'site-home',
    ),
    
    # Feeds
    url(
        regex   = '^feeds/(?P<url>.*)/$',           ## Feed for Recent Commits
        view    = feed,
        kwargs  = { 'feed_dict': feeds, },
        name    = 'project-feeds',
    ),
    
)
