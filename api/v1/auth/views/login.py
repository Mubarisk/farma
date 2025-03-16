from rest_framework.generics import CreateAPIView
from helpers.permissions import IsAuthenticatedUser
from django.core.cache import cache
from django.conf import settings
import jwt
from farma.config.response import SuccessResponse


class LogOutView(CreateAPIView):
    permission_classes = [IsAuthenticatedUser]

    def post(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        jwt_secret = settings.SECRET_KEY
        token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        jti = jwt.decode(token, jwt_secret, algorithms=["HS256"])["jti"]
        cache.delete(jti)
        return SuccessResponse(message="Successfully logged out")
