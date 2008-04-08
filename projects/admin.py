from django.contrib import admin

from models import Project, Developer, CodeRepository, CodeCommit


class CommitsInline(admin.TabularInline):
    model = CodeCommit
    extra = 3
    

class RepositoryInline(admin.TabularInline):
    model = CodeRepository
    extra = 1
    

class ProjectAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basics', {'fields': ('name', 'tagline', 'slug')}),
        ('Specifics', {'fields': ('active', 'url', 'description', 'tags')}),
        ('People', {'fields': ('owners', 'members')}),
    )
    inlines = [RepositoryInline]
    filter_horizontal = ('owners', 'members')
    list_display = ('name', 'url', 'active')
    search_fields = ('name', 'description')
    prepopulated_fields = { 'slug': ('name',) }
    

class DeveloperAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Metadata', {'fields': ('first_name', 'middle_name', 'last_name', 'suffix', 'svn_name', 'slug'), 'classes': ('wide',)}),
        ('URLs', {'fields': ('personal_url', 'professional_url', 'django_people_url'), 'classes': ('wide',)}),
    )
    list_display = ('full_name', 'svn_name', 'django_people_url')
    search_fields = ('last_name', 'first_name')
    prepopulated_fields = { 'slug': ('first_name', 'middle_name', 'last_name', 'suffix') }
    

class CodeRepositoryAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Linkage', {'fields': ('project',)}),
        ('Basics', {'fields': ('type', 'url')}),
        ('Optional', {'fields': ('public_changeset_template',), 'classes': ('collapse',)}),
    )
    inlines = [CommitsInline]
    list_display = ('__unicode__', 'type', 'url', 'public_changeset_template')
    search_fields = ('',)
    

class CodeCommitAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Linkage', {'fields': ('repository',)}),
        ('Basics', {'fields': ('revision', 'message', 'committed')}),
    )
    list_display = ('__unicode__', 'repository')
    list_filter = ('repository',)
    search_fields = ('message',)
    

admin.site.register(Project, ProjectAdmin)
admin.site.register(Developer, DeveloperAdmin)
admin.site.register(CodeRepository, CodeRepositoryAdmin)
admin.site.register(CodeCommit, CodeCommitAdmin)