from rest_framework.permissions import IsAuthenticated
from user.models import User
from django.core.cache import cache
from django.conf import settings
import jwt


class IsAuthenticatedUser(IsAuthenticated):
    def has_permission(self, request, view):
        # Check if user is authenticated using the parent class
        if not request.user.is_anonymous and super(
            IsAuthenticatedUser, self
        ).has_permission(request, view):

            jwt_secret = settings.SECRET_KEY

            auth_header = request.META.get("HTTP_AUTHORIZATION", "")

            token = auth_header.split()[1]
            try:
                decoded_token = jwt.decode(
                    token, jwt_secret, algorithms=["HS256"]
                )
                jti = decoded_token.get("jti")
                if not jti:
                    return False

                if cache.get(jti):
                    return True

                return False
            except Exception as e:
                return False

        return False


class IsAdmin(IsAuthenticatedUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.role == User.ADMIN
        return False


class IsStoreManager(IsAuthenticatedUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.role == User.STORE_MANAGER

        return False


class IsStaff(IsAuthenticatedUser):
    def has_permission(self, request, view):
        if super().has_permission(request, view):
            return request.user.role == User.STAFF
        return False
