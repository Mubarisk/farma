from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.cache import cache


class TokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        super().validate(attrs)
        refresh = self.get_token(self.user)
        access = refresh.access_token
        jti = access["jti"]
        cache.set(jti, self.user.id, timeout=360000)
        return {"access": str(access), "refresh": str(refresh)}
