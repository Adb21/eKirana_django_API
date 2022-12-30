from asyncio.windows_events import NULL
from cProfile import Profile
from email.policy import default
from msilib.schema import Class
import uuid
from pyexpat import model
from sre_constants import CHCODES
from django.db import models
from django.contrib.auth.models import User
from Product.models import Product
from django.db.models.signals import pre_save,pre_delete,post_save
from django.dispatch import receiver
from datetime import datetime
from Shop.models import Shop_OrderInventory
from .testEmail import sendMail
import threading


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

    class Meta:
        ordering = ['-Item']



class Order(models.Model):
    RefrenceID = models.CharField(max_length=30)
    User = models.ForeignKey(User,on_delete=models.CASCADE)
    Total = models.FloatField()
    status = models.IntegerField(choices=ORDER_STATUS,default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.id)

class OrderItems(models.Model):
    Order = models.ForeignKey(Order,on_delete=models.CASCADE) # on_delete=models.PROTECT
    Seller = models.ForeignKey("Shop.Shopkeeper",on_delete=models.CASCADE) # on_delete=models.PROTECT
    Item = models.ForeignKey(Product,on_delete=models.CASCADE)  # on_delete=models.PROTECT
    ItemRefID = models.CharField(max_length=50)
    Quantity = models.IntegerField()
    Price = models.FloatField()
    Total = models.FloatField()
    status = models.IntegerField(choices=ITEM_STATUS,default=0)
    
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
    return refid

def generateItemRefID():
    id = uuid.uuid1()
    refid = "IRF"+str(id.hex)
    return refid

@receiver(post_save,sender=Cart)
def placeOrder(sender,**kwargs):
    cart = kwargs['instance']
    if cart.Status :
        order = Order.objects.create(User=cart.User,RefrenceID=str(generateRefID()),Total=cart.Total)
        cis = CartItems.objects.filter(Cart=cart)
        for ci in cis:
            product = Product.objects.get(id=ci.Item.id)
            if product.Stock > 10:
                product.Stock = product.Stock - ci.Quantity
            product.save()
            itemref = str(generateItemRefID())
            OrderItems.objects.create(Order=order,ItemRefID=itemref,Seller=product.Shop,Item=ci.Item,Quantity=ci.Quantity,Price=ci.Item.Price,Total=ci.Price)
            Shop_OrderInventory.objects.create(Seller=product.Shop,Buyer=cart.User,Order=order,RefrenceID=order.RefrenceID,ItemRefID=itemref,Item=ci.Item,Stock=product.Stock,Price=ci.Item.Price,Total=ci.Price) 
        user = User.objects.get(username=cart.User)
        totalItems = OrderItems.objects.filter(Order=order).count()
        items = OrderItems.objects.filter(Order=order)
        orderList = []
        for i in items:
            orderList.append((i.Item.Title,i.Quantity))
        data = {'Username':user.username,'OrderNumber':order.RefrenceID,'TotalItems':totalItems,'OrderDetails':orderList,'TotalPrice':order.Total}
        #sendMail(str(user.email),data,0)
        t1 = threading.Thread(target=sendMail, args=(str(user.email),data,0))
        t1.start()
        # t1.join()

@receiver(pre_save,sender=Shop_OrderInventory)
def changeOrderItemStatus(sender,**kwargs):
    soi = kwargs['instance']
    orderitem = OrderItems.objects.get(ItemRefID=soi.ItemRefID)
    if orderitem.status == 0:
        orderitem.status = soi.status
    elif orderitem.status == 1 :
        if soi.status == 1 or soi.status == 2:
            orderitem.status = soi.status
    elif orderitem.status == 2:
         if soi.status == 2:
             orderitem.status = soi.status
    orderitem.save()


@receiver(post_save,sender=OrderItems)
def changeOrderStatus(sender,**kwargs):
    oi = kwargs['instance']
    orderitems = OrderItems.objects.filter(Order=oi.Order)
    flag = False
    for orderitem in orderitems:
        if orderitem.status == 1:
            oobj = Order.objects.get(id=oi.Order.id)
            oobj.status = 1
            oobj.save()
            break
        elif orderitem.status == 2:
            flag = True
        else:
            flag = False
            break

    if flag:
        oobj = Order.objects.get(id=oi.Order.id)
        oobj.status = 2
        oobj.save()
        user = User.objects.get(username=oobj.User)
        totalItems = OrderItems.objects.filter(Order=oobj).count()
        items = OrderItems.objects.filter(Order=oobj)
        orderList = []
        for i in items:
            orderList.append((i.Item.Title,i.Quantity))
        data = {'Username':user.username,'OrderNumber':oobj.RefrenceID,'TotalItems':totalItems,'OrderDetails':orderList,'TotalPrice':oobj.Total}
        #sendMail(str(user.email),data,1)
        t1 = threading.Thread(target=sendMail, args=(str(user.email),data,1))
        t1.start()
        

