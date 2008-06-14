from django.contrib import admin

from tagging.models import Tag, TaggedItem


admin.site.register(Tag)
admin.site.register(TaggedItem)