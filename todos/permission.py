from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """
    控制用户只能读写删除自己的todos
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # if request.method in permissions.SAFE_METHODS:
        #     return True

        # 只允许owner
        return obj.owner == request.user

