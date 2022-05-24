from attr import fields
from rest_framework import serializers
from .models import Shopkeeper
from drf_queryfields import QueryFieldsMixin
from Profile.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
import jwt
from rest_framework.authentication import get_authorization_header


#QueryFieldsMixin : helps in retriving selected data 
class ShopSerializer(QueryFieldsMixin,serializers.ModelSerializer):

    class Meta :
        model = Shopkeeper
        exclude = ['User']
        extra_kwargs = {
            'User_id': {'write_only': True},
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

    def validate(self, attrs):
        user_id = self.get_Userid(self.context.get('request'))
        if not Profile.objects.filter(User_id=user_id,User_Type='Seller').exists():
            msg = {"error":"User is not Seller"}
            raise serializers.ValidationError(msg)
        attrs['User_id'] = user_id
        return super().validate(attrs)


