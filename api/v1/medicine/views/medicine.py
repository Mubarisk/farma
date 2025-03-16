from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from helpers.permissions import IsStoreManager
from medicine.models import Medicine, MedicineCategory
from ..serializers import MedicineCategorySerializer, MedicineSerializer
from django.utils import timezone
from farma.config.response import SuccessResponse


class MedicineCategoryListCreateAPIView(ListCreateAPIView):
    queryset = MedicineCategory.objects.all().order_by("-id")
    serializer_class = MedicineCategorySerializer
    permission_classes = [IsStoreManager]


class MedicineCategoryRetrieveUpdateDestroyAPIView(
    RetrieveUpdateDestroyAPIView
):
    queryset = MedicineCategory.objects.all()
    serializer_class = MedicineCategorySerializer
    permission_classes = [IsStoreManager]


class MedicineListCreateAPIView(ListCreateAPIView):
    queryset = (
        Medicine.objects.prefetch_related("packages")
        .filter(is_deleted=False)
        .order_by("-id")
    )
    serializer_class = MedicineSerializer
    permission_classes = [IsStoreManager]


class MedicineRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.prefetch_related("packages").filter(
        is_deleted=False
    )
    serializer_class = MedicineSerializer
    permission_classes = [IsStoreManager]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_deleted = True
        instance.deleted_at = timezone.now()
        instance.save(update_fields=["is_deleted", "deleted_at"])
        return SuccessResponse(
            message="Medicine deleted successfully.", status=200
        )
