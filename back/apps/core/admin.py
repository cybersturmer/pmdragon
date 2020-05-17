from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import *


class PersonInlineAdmin(admin.StackedInline):
    model = Person
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (PersonInlineAdmin,)


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    model = Person


@admin.register(PersonRegistrationRequest)
class PersonRegistrationRequestAdmin(admin.ModelAdmin):
    model = PersonRegistrationRequest
    readonly_fields = ('key',)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
