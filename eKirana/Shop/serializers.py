from attr import fields
from rest_framework import serializers
from Profile.serializers import UserSerializer
from Order.serializers import OrderSerializer
from .models import Shopkeeper,Shop_OrderInventory
from drf_queryfields import QueryFieldsMixin
from Profile.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
import jwt
from rest_framework.authentication import get_authorization_header
from rest_framework.pagination import PageNumberPagination


#QueryFieldsMixin : helps in retriving selected data 
class ShopSerializer(QueryFieldsMixin,serializers.ModelSerializer):

    User = UserSerializer
    class Meta :
        model = Shopkeeper
        exclude = ['User']
        #fields = '__all__'
        extra_kwargs = {
            'User_id': {'write_only': True},
        }

    def validate(self, attrs):
        user_id = get_Userid(self.context.get('request'))
        if not Profile.objects.filter(User_id=user_id,User_Type=1).exists():
            msg = {"error":"User is not Seller"}
            raise serializers.ValidationError(msg)
        return super().validate(attrs)

class InventorySummarySerializer(serializers.ModelSerializer):
    Buyer = UserSerializer
    Seller = ShopSerializer
    Order = OrderSerializer
    class Meta:
        model = Shop_OrderInventory
        exclude = ['Seller','Buyer','Item','Stock','Price']
        #fields = '__all__'
        # extra_kwargs = {
        #     'User_id': {'write_only': True},
        # }
        
class ShopInventorySerializer(serializers.ModelSerializer):
    Buyer = UserSerializer
    Seller = ShopSerializer
    Order = OrderSerializer
    class Meta:
        model = Shop_OrderInventory
        exclude = ['Seller']
        #fields = '__all__'
        # extra_kwargs = {
        #     'User_id': {'write_only': True},
        # }
        
def get_Userid(request):
    try :
        token = get_authorization_header(request).decode('utf-8')
        #print(token[7:])
        payload = jwt.decode(token[7:],  algorithms=['HS256'],options={"verify_signature": False}) 
        user_id = payload['user_id']
    except :
        msg = {"error":"Header not found"}
        raise serializers.ValidationError(msg)
    return user_id

def getUserType(uid):
    if Profile.objects.filter(User=uid).exists():
        profile = Profile.objects.get(User=uid)
        return profile.User_Type
    msg = {"error":"User Not Found"}
    raise serializers.ValidationError(msg)

def getShop(uid):
    if Shopkeeper.objects.filter(User=uid).exists():
        shop = Shopkeeper.objects.get(User=uid)
        return shop.id
    msg = {"error":"Shop Not Found"}
    raise serializers.ValidationError(msg)