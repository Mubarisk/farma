from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("medicine/", include("api.v1.medicine.urls")),
    path("billing/", include("api.v1.billing.urls")),
    path("dashboard/", include("api.v1.dashboard.urls")),
]
