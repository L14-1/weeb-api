from rest_framework.permissions import BasePermission, SAFE_METHODS
from auth_app.models import Profile, Role


class IsOwnerOrAdminOrReadOnly(BasePermission):
    """
    - Lecture publique
    - Création réservée aux users authentifiés
    -Modification + suppression réservé au Owner ou à un admin
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if obj.owner_id == request.user.id:
            return True

        try:
            role = request.user.profile.role
        except Profile.DoesNotExist:
            role = None

        return bool(
            request.user.is_staff
            or request.user.is_superuser
            or role == Role.ADMIN
        )