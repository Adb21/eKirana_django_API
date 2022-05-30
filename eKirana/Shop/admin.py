import imp
from django.contrib import admin
from .models import Shopkeeper,Shop_OrderInventory

# Register your models here.
admin.site.register(Shopkeeper)
admin.site.register(Shop_OrderInventory)
