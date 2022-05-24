from .serializers import UserSerializer,UserLoginSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status,generics
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.
class RegisterUserAPIView(generics.GenericAPIView):
    serializer_class = UserSerializer
    
    def post(self,request):
        serializer  = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message":"User Registerd Successfully",
                    "Username":serializer.data['username']
                    # "tokens":serializer.data['tokens']

                },status=status.HTTP_201_CREATED
            )
        return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class LoginUserAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    
    def post(self,request):
        serializer  = UserLoginSerializer(data=request.data,context={ 'request': self.request })
        if serializer.is_valid():
            return Response(
                {
                    "Message":"User Login Successfully",
                    "Username":serializer.data['username'],
                    "tokens":serializer.data["tokens"]

                },status=status.HTTP_202_ACCEPTED
            )
        return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    



