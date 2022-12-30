from sre_constants import CHCODES
from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from Profile.models import Profile
# from Order.models import Order

# Create your models here.
ORDER_STATUS = ((0,"Pending"),(1,"Accepted"),(2,"Completed"))
STATE_CHOICES = (("Andhra Pradesh","Andhra Pradesh"),("Arunachal Pradesh ","Arunachal Pradesh "),("Assam","Assam"),("Bihar","Bihar"),("Chhattisgarh","Chhattisgarh"),("Goa","Goa"),("Gujarat","Gujarat"),("Haryana","Haryana"),("Himachal Pradesh","Himachal Pradesh"),("Jammu and Kashmir ","Jammu and Kashmir "),("Jharkhand","Jharkhand"),("Karnataka","Karnataka"),("Kerala","Kerala"),("Madhya Pradesh","Madhya Pradesh"),("Maharashtra","Maharashtra"),("Manipur","Manipur"),("Meghalaya","Meghalaya"),("Mizoram","Mizoram"),("Nagaland","Nagaland"),("Odisha","Odisha"),("Punjab","Punjab"),("Rajasthan","Rajasthan"),("Sikkim","Sikkim"),("Tamil Nadu","Tamil Nadu"),("Telangana","Telangana"),("Tripura","Tripura"),("Uttar Pradesh","Uttar Pradesh"),("Uttarakhand","Uttarakhand"),("West Bengal","West Bengal"),("Andaman and Nicobar Islands","Andaman and Nicobar Islands"),("Chandigarh","Chandigarh"),("Dadra and Nagar Haveli","Dadra and Nagar Haveli"),("Daman and Diu","Daman and Diu"),("Lakshadweep","Lakshadweep"),("National Capital Territory of Delhi","National Capital Territory of Delhi"),("Puducherry","Puducherry"))

class Shopkeeper(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Shop_Name = models.CharField(max_length=100) 
    Contact = models.BigIntegerField()
    Locality = models.CharField(max_length=30)
    State = models.CharField(choices=STATE_CHOICES,max_length=50)
    City = models.CharField(max_length=50)
    Pincode = models.IntegerField()
    
    def __str__(self):
        return str(self.Shop_Name)

class Shop_OrderInventory(models.Model):
    Seller = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    Buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    Order = models.ForeignKey("Order.Order",on_delete=models.CASCADE)
    RefrenceID = models.CharField(max_length=50)
    ItemRefID = models.CharField(max_length=50)
    status = models.IntegerField(choices=ORDER_STATUS,default=0)   
    Item = models.ForeignKey(Product, on_delete=models.CASCADE)
    Stock = models.IntegerField()
    Price = models.FloatField()
    Total = models.FloatField()

    def __str__(self):
        return str(self.Order)