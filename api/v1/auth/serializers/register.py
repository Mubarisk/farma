from rest_framework import serializers

from user.models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "role", "password")

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
