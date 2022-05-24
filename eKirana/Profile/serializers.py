from rest_framework import serializers
from .models import Profile
from drf_queryfields import QueryFieldsMixin
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
import jwt


#QueryFieldsMixin : helps in retriving selected data 
class ProfileSerializer(QueryFieldsMixin,serializers.ModelSerializer):
    class Meta :
        model = Profile
        fields = ['Mobile','User_Type','Locality','State','City','Pincode']

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 50, min_length = 8, write_only = True)
    email = serializers.EmailField(max_length = 50)
    first_name = serializers.CharField(max_length = 100)
    last_name = serializers.CharField(max_length = 100)
    tokens = serializers.SerializerMethodField()
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = ['username', 'email','password', 'first_name', 'last_name','tokens','profile']

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        data = {
            "refresh": refresh,
            "access": access,
        }
        return data

    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            msg = {"email error":"Email Already Exists"}
            raise serializers.ValidationError(msg)
        return super().validate(attrs)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        user =  User.objects.create_user(**validated_data)
        Profile.objects.create(
            User=user,
            Mobile=profile_data['Mobile'],
            User_Type=profile_data['User_Type'],
            Locality=profile_data['Locality'],
            State=profile_data['State'],
            City=profile_data['City'],
            Pincode=profile_data['Pincode']
        )
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=255)
    tokens = serializers.DictField(read_only=True)

    class Meta:
        model = User
        fields = ['username','password','tokens']

    def get_tokens(self, user):
        tokens = RefreshToken.for_user(user)
        refresh = str(tokens)
        access = str(tokens.access_token)
        # payload = jwt.decode(access,  algorithms=['HS256'],options={"verify_signature": False}) 
        # payload['user_type'] = "test_type"
        # access =  jwt.encode(payload,'secret',algorithm='HS256')
        data = {
            "refresh": refresh,
            "access": access
        }
        return data
        
    def validate(self, attrs):
        username = attrs["username"]
        password = attrs["password"]

        user = authenticate(request=self.context.get('request'),username=username, password=password)
        if user is None:
            msg = {"User error":"Invalid Credentials. User Not Found"}
            raise serializers.ValidationError(msg)
        update_last_login(None, user)
        attrs["tokens"] = self.get_tokens(user)
        attrs["username"] = user.username
        return super().validate(attrs)






        

