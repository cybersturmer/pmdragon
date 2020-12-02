from rest_framework import permissions

from apps.core.models import Person


class IsCreatorOrReadOnly(permissions.BasePermission):
    """
    Allow update / remove to object only if current user
    is determined as an owner in created_by field.
    For others this permission allow only read access.
    We use it for example in IssueMessages.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.created_by == request.user.person


class IsParticipateInWorkspace(permissions.BasePermission):
    """
    Allow access to object if object workspace do not determined
    Or current user participate in workspace
    """
    def has_object_permission(self, request, view, obj):
        return not hasattr(obj, 'workspace') or request.user.person in obj.workspace.participants.all()


class IsMeOrReadOnly(permissions.BasePermission):
    """
    Allow access to Person if its me.
    Reject update / delete for others
    We will use it in all Person related views.
    """
    def has_object_permission(self, request, view, obj: Person):
        return request.user.person == obj
