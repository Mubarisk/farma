from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import path
from .views import UserRegisterView, LogOutView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view()),
    path("register/", UserRegisterView.as_view()),
    path("logout/", LogOutView.as_view()),
]
