from django.contrib import admin

from models import Item


class ItemAdmin(admin.ModelAdmin):
    date_hierarchy = 'timestamp'
    list_display = ('timestamp', 'object_str')
    list_filter = ('content_type', 'timestamp')
    search_fields = ('object_str', 'tags')
    

admin.site.register(Item, ItemAdmin)