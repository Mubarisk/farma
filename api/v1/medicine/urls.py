from django.urls import path
from .views import (
    MedicineCategoryListCreateAPIView,
    MedicineCategoryRetrieveUpdateDestroyAPIView,
    MedicineListCreateAPIView,
    MedicineRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("categories/", MedicineCategoryListCreateAPIView.as_view()),
    path(
        "categories/<int:pk>/",
        MedicineCategoryRetrieveUpdateDestroyAPIView.as_view(),
    ),
    path("", MedicineListCreateAPIView.as_view()),
    path("<int:pk>/", MedicineRetrieveUpdateDestroyAPIView.as_view()),
]
