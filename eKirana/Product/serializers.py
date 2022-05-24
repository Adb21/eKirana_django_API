import imp
from rest_framework import serializers
from .models import Product
from drf_queryfields import QueryFieldsMixin
from Profile.models import Profile
from Shop.models import Shopkeeper
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
import jwt
from rest_framework.authentication import get_authorization_header


#QueryFieldsMixin : helps in retriving selected data 
class ProductSerializer(QueryFieldsMixin,serializers.ModelSerializer):

    class Meta :
        model = Product
        exclude = ['Shop']
        #fields = '__all__'
        extra_kwargs = {
            'Shop_id': {'write_only': True},
        }

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

    def _isSeller(self,request):
        user_id = self.get_Userid(request)
        if not Profile.objects.filter(User_id=user_id,User_Type=1).exists():
            msg = {"error":"User is not Seller"}
            raise serializers.ValidationError(msg)

        return True

    def validate(self, attrs):
        uid = self.get_Userid(self.context.get('request'))
        if self._isSeller(self.context.get('request')):
            if not Shopkeeper.objects.filter(User=uid).exists():
                msg = {"error":"Shop with user not Found. Please register Shop first."}
                raise serializers.ValidationError(msg)
            shopkeeper =  Shopkeeper.objects.get(User=uid)
            attrs["Shop_id"] = shopkeeper.id
                        
        return super().validate(attrs)


