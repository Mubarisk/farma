from rest_framework.generics import CreateAPIView
from ..serializers import UserRegisterSerializer
from helpers.permissions import IsAdmin


class UserRegisterView(CreateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = UserRegisterSerializer
