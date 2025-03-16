from django.urls import path
from .views import StockAvailabilityAPIView, SalesReportsAPIView

urlpatterns = [
    path("stock/", StockAvailabilityAPIView.as_view()),
    path("reports/", SalesReportsAPIView.as_view()),
]
