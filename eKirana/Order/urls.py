from django import views
from django.contrib import admin
from django.db import router
from django.urls import path,include
from .views import CarListAPIVIew
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('products',ProductAPIView,basename="product")

urlpatterns = [
    path('', CarListAPIVIew.as_view(), name='cart'),
]