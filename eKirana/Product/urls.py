from django import views
from django.contrib import admin
from django.db import router
from django.urls import path,include
from .views import ProductListAPIView,ProductCreateAPIView,ProductRetriveAPIView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('products',ProductAPIView,basename="product")

urlpatterns = [
    path('', ProductListAPIView.as_view(), name='products'),
    path('<int:pk>', ProductRetriveAPIView.as_view(), name='Retrieve product'),
    path('add', ProductCreateAPIView.as_view(), name='add products'),
]