from sre_constants import CHCODES
from django.db import models
from django.contrib.auth.models import User
from Profile.models import Profile

# Create your models here.
USER_TYPE = (
    ("Customer", "Customer"),
    ("Seller", "Seller"),
)

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