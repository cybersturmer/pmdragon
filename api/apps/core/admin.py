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


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    model = Project


@admin.register(IssueTypeCategory)
class IssueTypeCategoryAdmin(admin.ModelAdmin):
    model = IssueTypeCategory


@admin.register(IssueStateCategory)
class IssueStateCategoryAdmin(admin.ModelAdmin):
    model = IssueStateCategory


@admin.register(Issue)
class Issue(admin.ModelAdmin):
    model = Issue


@admin.register(ProjectBacklog)
class ProjectBacklog(admin.ModelAdmin):
    model = ProjectBacklog


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
