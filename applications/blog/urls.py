from django.conf.urls.defaults import *
from django.views.decorators.cache import cache_page
from django.views.generic import date_based, list_detail
from django.contrib.syndication.views import feed

from models import Entry
from feeds import LatestEntries


# Feeds
feeds = {
  'latest-entries': LatestEntries,
}


# Querysets
entries = {
    'queryset': Entry.live.all(),
    'date_field': 'published',
    'template_object_name': 'entry',
}

entries_index = {
    'queryset': Entry.live.all(),
    'date_field': 'published',
    'template_object_name': 'entry',
    'num_latest': 10,
}

entries_year = {
    'queryset': Entry.live.all(),
    'date_field': 'published',
    'template_object_name': 'entry',
    'make_object_list': True,
}

detail = {
    'queryset': Entry.live.all(),
    'date_field': 'published',
    'slug_field': 'slug',
    'template_object_name': 'entry',
}


# URL Configuration
urlpatterns = patterns('',

    # Post Page (Must be first!)
    url(
        regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
        view    = date_based.object_detail,
        kwargs  = detail,
        name    = 'entry-detail',
    ),
    
    # Archive URLs
    url(
        regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$',
        view    = date_based.archive_day,
        kwargs  = entries,
        name    = 'archive-day',
    ),
    url(
        regex   = '^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
        view    = date_based.archive_month,
        kwargs  = entries,
        name    = 'archive-month',
    ),    
    url(
        regex   = '(?P<year>\d{4})/$',
        view    = date_based.archive_year,
        kwargs  = entries_year,
        name    = 'archive-year',
    ),
    url(
        regex   = '^$',
        view    = date_based.archive_index,
        kwargs  = entries_index,
        name    = 'archive-index',
    ),
    
    # Feed URLs
    url(
        regex   = '^feeds/(?P<url>.*)/$',
        view    = feed,
        kwargs  = { 'feed_dict': feeds },
        name    = 'blog-feeds',
    )
    
)

