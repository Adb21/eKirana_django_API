from django.contrib import admin
from django.urls import path
from .views import ShopAPIView,ShopInventoryAPIView,ChangeOrderStatusAPIView

urlpatterns = [
    path('register', ShopAPIView.as_view(), name='shop_register'),
    path('', ShopAPIView.as_view(), name='Shops'),
    path('<int:pk>', ShopAPIView.as_view(), name='Shop'),
    path('inventory', ShopInventoryAPIView.as_view(), name='Shop inventory'),
    path('inventory/<int:pk>', ShopInventoryAPIView.as_view(), name='Shop inventory'),
    path('inventory/<int:pk>/status', ChangeOrderStatusAPIView.as_view(), name='order status')
]