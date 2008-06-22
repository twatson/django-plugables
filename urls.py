from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import list_detail
from django.views.generic.simple import direct_to_template, redirect_to
from django.contrib.sitemaps import GenericSitemap
from django.contrib import admin

from blog.urls import entries
from projects.urls import project_list, repository_list, developer_list


# Sitemaps
sitemaps = {
    'blog': GenericSitemap(entries, priority=0.6),
    'projects': GenericSitemap(project_list, priority=0.7),
    'developers': GenericSitemap(developer_list, priority=0.7),
}


# URL Patterns
urlpatterns = patterns('',
    
    # Nuts and Bolts
    (r'^', include('projects.urls')),
    
    # Blog
    (r'^blog/', include('blog.urls')),
    
    # Contact Form / About
    (r'^about/', include('contact_form.urls')),
    
    # Sitemaps
    (r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
    
    # Administration
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    ('^admin/(.*)', admin.site.root),
    
)
