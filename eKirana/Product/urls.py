from django import views
from django.contrib import admin
from django.db import router
from django.urls import path,include
from .views import ProductListAPIVIew,ProductCreateAPIView,ProductRetriveAPIVIew
from rest_framework.routers import DefaultRouter

# router = DefaultRouter()
# router.register('products',ProductAPIView,basename="product")

urlpatterns = [
    path('', ProductListAPIVIew.as_view(), name='products'),
    path('<int:pk>', ProductRetriveAPIVIew.as_view(), name='Retrieve product'),
    path('add', ProductCreateAPIView.as_view(), name='add products'),
    # path('',include(router.urls))
]