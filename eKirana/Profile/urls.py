from django.contrib import admin
from django.urls import path
from .views import RegisterUserAPIView,LoginUserAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/register', RegisterUserAPIView.as_view(), name='register'),
    path('api/login', LoginUserAPIView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]