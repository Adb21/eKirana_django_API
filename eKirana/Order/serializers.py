from genericpath import exists
from rest_framework import serializers
from Product.serializers import ProductSerializer
from Profile.models import Profile
from .models import Cart,CartItems
from Profile.serializers import UserSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
import jwt
from rest_framework.authentication import get_authorization_header


#QueryFieldsMixin : helps in retriving selected data 
class CartSerializer(serializers.ModelSerializer):
    User = UserSerializer
    class Meta :
        model = Cart
        fields = '__all__'

    def get_Userid(self,request):
        try :
            token = get_authorization_header(request).decode('utf-8')
            #print(token[7:])
            payload = jwt.decode(token[7:],  algorithms=['HS256'],options={"verify_signature": False}) 
            user_id = payload['user_id']
        except :
            msg = {"error":"Header not found"}
            raise serializers.ValidationError(msg)
        return user_id

    def validate(self, attrs):
        uid = self.get_Userid(self.context.get('request'))
        if Profile.objects.filter(User_id=uid,User_Type=1).exists():
            msg = {"error":"User is Seller.Seller Cannot buy products"}
            raise serializers.ValidationError(msg)
        return super().validate(attrs)


class CartItemSerializer(serializers.ModelSerializer):
    Cart = CartSerializer
    Item = ProductSerializer
    Quantity = serializers.IntegerField(max_value=10)

    class Meta :
        model = CartItems
        # fields = '__all__'
        exclude = ['Cart']
        extra_kwargs = {'Quantity': {'required': True}} 


    def create(self, validated_data):
        item_data = validated_data.pop("Item")
        qty = validated_data.pop("Quantity")
        if not checkQty(qty):
            msg = {"error":"Invalid Quantity"}
            raise serializers.ValidationError(msg)
        uid = get_Userid(self.context.get('request'))
        if not Cart.objects.filter(User_id=uid).exists():
            cart = Cart.objects.create(User_id=uid)
        else:
            cart = Cart.objects.get(User_id=uid)
        if CartItems.objects.filter(Cart=cart,Item=item_data).exists():
            item = CartItems.objects.get(Cart=cart,Item=item_data)
            item.Quantity = item.Quantity + qty
            if item.Quantity > 10:
                msg = {"error":"Quantity greater than 10 not allowed"}
                raise serializers.ValidationError(msg)
            elif item.Quantity == 0:
                item.delete()
            elif item.Quantity < 0 :
                msg = {"error":"Quantity cannot be negative"}
                raise serializers.ValidationError(msg)
            else:
                item.save()
        else:
            if qty == -1:
                msg = {"error":"Item cannot be created using negative quantity"}
                raise serializers.ValidationError(msg)
            item = CartItems.objects.create(Cart=cart,Item=item_data,Quantity=qty)
        return item

def get_Userid(request):
    try :
        token = get_authorization_header(request).decode('utf-8')
        #print(token[7:])
        payload = jwt.decode(token[7:],  algorithms=['HS256'],options={"verify_signature": False}) 
        user_id = payload['user_id']
    except :
        msg = {"error":"Header not found in metohd"}
        raise serializers.ValidationError(msg)
    return user_id

def get_Cart(uid):
    if Cart.objects.filter(User_id=uid).exists():
        cart = Cart.objects.get(User_id=uid)
        return cart
    else:
        # msg = {"error":"User with Cart Not Found"}
        # raise serializers.ValidationError(msg)
        # cart = Cart(User=uid)
        # cart.save()
        return -1

def checkQty(qty):
    if qty < -1:
        return False
    return True
