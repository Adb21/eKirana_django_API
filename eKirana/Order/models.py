from asyncio.windows_events import NULL
import imp
from pyexpat import model
from sre_constants import CHCODES
from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from django.db.models.signals import pre_save,pre_delete,post_save
from django.dispatch import receiver

# Create your models here.
class Cart(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    Status = models.BooleanField(default=False)
    Total = models.FloatField(default=0.0)

    def __str__(self):
        return self.User.username+" "+str(self.id)

class CartItems(models.Model):
    Cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    Item = models.ForeignKey(Product,on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=0)
    Price = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.id) +" "+ str(self.Item)

    
@receiver(pre_save,sender=CartItems)
def correctPrice(sender,**kwargs):
    cart_item = kwargs['instance']
    product = Product.objects.get(id = cart_item.Item.id)
    total_qty_price = cart_item.Quantity * float(product.Price)
    cart_item.Price = total_qty_price


@receiver(post_save,sender=CartItems)
def correctPrice(sender,**kwargs):
    cart_item = kwargs['instance']
    cart = Cart.objects.get(id=cart_item.Cart.id)
    items = CartItems.objects.filter(Cart_id=cart.id)
    cart.Total = sum([item.Price for item in items])
    cart.save() 

@receiver(pre_delete,sender=CartItems)
def correctPrice_afterdelete(sender,**kwargs):
    cart_item = kwargs['instance']
    cart = Cart.objects.get(id=cart_item.Cart.id)
    cart.Total = cart.Total - cart_item.Price
    cart.save()







