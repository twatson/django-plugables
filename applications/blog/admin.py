from django.contrib import admin

from models import Entry


class EntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'published'
    fieldsets = (
        ('Metadata', {'fields': ('title', 'slug', 'published', 'author')}),
        ('Content', {'fields': ('summary', 'body', 'footnotes')}),
        ('Options', {'fields': ('status', 'enable_comments')}),
    )
    list_display = ('title', 'status', 'slug', 'published', 'enable_comments')
    list_filter = ('published', 'status')
    prepopulated_fields = { 'slug': ('title',) }
    search_fields = ('title', 'summary', 'body', 'footnotes')
    

admin.site.register(Entry, EntryAdmin)