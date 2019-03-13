from rest_framework.permissions import BasePermission


class AnonUserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action == 'create':
            return view.basename == 'user'
        else:
            return False


class AuthUserPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action == 'create':
            return False
        elif view.action == 'update':
            return True
        elif view.action == 'destroy':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action == 'update':
            return request.user == obj
        elif view.action == 'destroy':
            return request.user == obj
        else:
            return False


class AnonPostPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'retrieve':
            return True
        else:
            return False


class AuthPostPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action == 'create':
            return request.user.id == int(view.kwargs['user_pk'])
        elif view.action == 'update':
            return True
        elif view.action == 'destroy':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action == 'update':
            return request.user.id == obj.user.id
        elif view.action == 'destroy':
            return request.user.id == obj.user.id
        else:
            return False


class AnonLikePermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'retrieve':
            return True
        else:
            return False


class AuthLikePermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'retrieve':
            return True
        elif view.action == 'create':
            return True
        elif view.action == 'destroy':
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif view.action == 'destroy':
            return request.user.id == obj.user.id
        else:
            return False
