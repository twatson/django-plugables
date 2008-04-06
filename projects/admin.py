from django.contrib import admin

from models import Project, Maintainer, CodeRepository, CodeCommit


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'url')
    search_fields = ('name', 'description')
    prepopulated_fields = { 'slug': ('name',) }
    

class MaintainerAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
    search_fields = ('last_name', 'first_name', 'bio')
    prepopulated_fields = { 'slug': ('first_name', 'middle_name', 'last_name', 'suffix') }
    

class CodeRepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'url')
    search_fields = ('',)
    prepopulated_fields = { 'slug': ('name',) }
    

class CodeCommitAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'repository')
    list_filter = ('repository',)
    search_fields = ('message',)
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(Maintainer, MaintainerAdmin)
admin.site.register(CodeRepository, CodeRepositoryAdmin)
admin.site.register(CodeCommit, CodeCommit)