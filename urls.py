from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib import admin

from projects.models import Project, CodeRepository, Developer


# Querysets
project_list = {
    'queryset': Project.objects.select_related(),
    'template_object_name': 'project',
    'extra_context': {
        'owners': Developer.objects.filter()
    }
}

project_detail = {
    'queryset': Project.objects.select_related(),
    'template_object_name': 'project',
    
}

developer_list = {
    'queryset': Developer.objects.all(),
    'template_object_name': 'developer',
    'extra_context': {
        'count': Developer.objects.count,
    }
}

developer_detail = {
    'queryset': Developer.objects.all(),
    'template_object_name': 'developer',

}

repository_list = {
    'queryset': CodeRepository.objects.all(),
    'template_object_name': 'repository',
    
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
    
    # Homepage
    url(
        regex   = '^$',
        view    = direct_to_template,
        kwargs  = { 'template': 'home.html' },
        name    = 'site-home',
    ),
    
    # Administration
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/(.*)', admin.site.root),
)
