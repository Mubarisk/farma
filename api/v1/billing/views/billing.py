from rest_framework.generics import CreateAPIView
from helpers.permissions import IsStaff
from ..serializers import BillSerializer


class BillCreateAPIView(CreateAPIView):
    serializer_class = BillSerializer
    permission_classes = [IsStaff]
