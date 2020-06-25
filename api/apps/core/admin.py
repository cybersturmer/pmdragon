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
        'workspace',
        'title',
        'is_default',
        'ordering'
    )
    save_as = True


@admin.register(IssueTypeCategory)
class IssueTypeAdmin(admin.ModelAdmin):
    model = IssueTypeCategory
    list_display = (
        'workspace',
        'title',
        'is_subtask',
        'is_default',
        'ordering'
    )


admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(ProjectBacklog)
admin.site.register(SprintDuration)
admin.site.register(Sprint)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
