from django import views
from django.contrib import admin
from django.db import router
from django.urls import path,include
from .views import CarListAPIView,BuyNowAPIView,OrderListAPIView
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('products',ProductAPIView,basename="product")

urlpatterns = [
    path('cart', CarListAPIView.as_view(), name='cart'),
    path('cart/buynow', BuyNowAPIView.as_view(), name='buynow'),
    path('orders', OrderListAPIView.as_view(), name='order'),
    path('orders/<int:pk>', OrderListAPIView.as_view(), name='order details'),
]