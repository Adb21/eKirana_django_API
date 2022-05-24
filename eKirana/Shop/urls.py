from django.contrib import admin
from django.urls import path
from .views import ShopAPIView

urlpatterns = [
    path('register', ShopAPIView.as_view(), name='shop_register'),
    path('', ShopAPIView.as_view(), name='Shops'),
    path('<int:pk>', ShopAPIView.as_view(), name='Shop'),
]