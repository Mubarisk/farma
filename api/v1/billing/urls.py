from django.urls import path
from .views import BillCreateAPIView

urlpatterns = [
    path("", BillCreateAPIView.as_view()),
]
