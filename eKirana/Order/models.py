from asyncio.windows_events import NULL
import imp
from pyexpat import model
from sre_constants import CHCODES
from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from django.db.models.signals import pre_save,pre_delete,post_save
from django.dispatch import receiver
from datetime import datetime
from Shop.models import Shop_OrderInventory

ORDER_STATUS = [(0,"Pending"),(1,"In Progress"),(2,"Completed")]
ITEM_STATUS = [(0,"Pending"),(1,"Accepted"),(2,"Completed")]
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

class Order(models.Model):
    RefrenceID = models.CharField(max_length=25)
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Total = models.FloatField()
    status = models.CharField(choices=ORDER_STATUS,default=ORDER_STATUS[0],max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class OrderItems(models.Model):
    Order = models.ForeignKey(Order,on_delete=models.CASCADE) # on_delete=models.PROTECT
    Seller = models.ForeignKey("Shop.Shopkeeper",on_delete=models.CASCADE) # on_delete=models.PROTECT
    Item = models.ForeignKey(Product,on_delete=models.CASCADE)  # on_delete=models.PROTECT
    Quantity = models.IntegerField()
    Price = models.FloatField()
    Total = models.FloatField()
    status = models.CharField(choices=ITEM_STATUS,default=ITEM_STATUS[0],max_length=20)
    
    def __str__(self):
        return str(self.Order)
    
@receiver(pre_save,sender=CartItems)
def correctPrice(sender,**kwargs):
    cart_item = kwargs['instance']
    product = Product.objects.get(id = cart_item.Item.id)
    total_qty_price = cart_item.Quantity * float(product.Price)
    cart_item.Price = total_qty_price

@receiver(post_save,sender=CartItems)
def correctPriceTotal(sender,**kwargs):
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

def generateRefID():
    now = datetime.now()
    refid = "RF"+str(now.strftime("%y%m%d")) +""+str(now.strftime("%M%S"))
    print(refid)
    return refid


@receiver(post_save,sender=Cart)
def placeOrder(sender,**kwargs):
    cart = kwargs['instance']
    print(type(cart))
    if cart.Status :
        order = Order.objects.create(User=cart.User,RefrenceID=str(generateRefID()),Total=cart.Total)
        cis = CartItems.objects.filter(Cart=cart)
        for ci in cis:
            product = Product.objects.get(id=ci.Item.id)
            OrderItems.objects.create(Order=order,Seller=product.Shop,Item=ci.Item,Quantity=ci.Quantity,Price=ci.Item.Price,Total=ci.Price)
            Shop_OrderInventory.objects.create(Seller=product.Shop,Buyer=cart.User,Order=order,RefrenceID=order.RefrenceID,Item=ci.Item,Stock=product.Stock,Price=ci.Item.Price,Total=ci.Price) 

    