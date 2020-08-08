from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *


class PersonInlineAdmin(admin.StackedInline):
    model = Person
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (PersonInlineAdmin,)


@admin.register(PersonRegistrationRequest)
class PersonRegistrationRequestAdmin(admin.ModelAdmin):
    model = PersonRegistrationRequest
    readonly_fields = ('key',)


@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    model = Workspace
    readonly_fields = ('created_at',)


@admin.register(IssueStateCategory)
class IssueStateAdmin(admin.ModelAdmin):
    model = IssueStateCategory
    list_display = (
        'project',
        'title',
        'is_default',
        'ordering'
    )
    save_as = True


@admin.register(IssueTypeCategory)
class IssueTypeAdmin(admin.ModelAdmin):
    model = IssueTypeCategory
    list_display = (
        'project',
        'title',
        'is_subtask',
        'is_default',
        'ordering'
    )
    save_as = True


@admin.register(SprintDuration)
class SprintDurationAdmin(admin.ModelAdmin):
    model = SprintDuration
    list_display = (
        'workspace',
        'title',
        'duration'
    )
    save_as = True


@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    model = Sprint
    list_display = (
        'project',
        'title',
        'goal',
        'started_at',
        'finished_at'
    )
    readonly_fields = ('workspace',)
    save_as = True

    def save_model(self, request, obj, form, change):
        obj.workspace = obj.project.workspace
        super(SprintAdmin, self).save_model(request, obj, form, change)


@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    model = Issue
    list_display = (
        'project',
        'title',
        'type_category',
        'state_category',
        'created_by'
    )
    readonly_fields = (
        'workspace',
    )
    search_fields = (
        'title'
    )
    
    def save_model(self, request, obj, form, change):
        obj.workspace = obj.project.workspace
        super(IssueAdmin, self).save_model(request, obj, form, change)


admin.site.register(Project)
admin.site.register(ProjectBacklog)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
