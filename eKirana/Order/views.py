from requests import request
from yaml import serialize

from rest_framework.views import APIView
from .serializers import CartItemSerializer, CartSerializer, get_Cart, get_Userid
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework import status,generics,viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from .models import CartItems,Cart
from rest_framework.response import Response

class CarListAPIVIew(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request):
        uid = get_Userid(request)
        cart = get_Cart(uid)
        if cart == -1:
            return Response({"Message":"Cart is Empty"},status=status.HTTP_200_OK )
        cart_items = CartItems.objects.filter(Cart_id=cart.id)
        serializer = CartItemSerializer(cart_items,many=True)
        return Response(
            {
                "Cart Total Price":cart.Total,
                "Cart Items" : serializer.data
            },status=status.HTTP_200_OK 
        )

    def post(self,request):
        data_serializer = CartItemSerializer(data=request.data,context={ 'request': self.request })
        if data_serializer.is_valid():
            z = data_serializer.save() 
            item = z.Item.Title
            if request.data["Quantity"] == -1:
                return Response(
                {
                    "Message":"Item "+str(item)+" removed from cart successfully",
                },status=status.HTTP_202_ACCEPTED
            )

            return Response(
                {
                    "Message":"Item "+str(item)+" added to cart successfully",
                },status=status.HTTP_202_ACCEPTED
            )
        return Response({"Error":data_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, format=None):
        uid = get_Userid(request)
        cart = get_Cart(uid)
        if cart == -1:
            return Response({"Message":"Cart is Empty"},status=status.HTTP_200_OK )
        cart.delete()
        return Response({"Message":"Cleared Cart Successfully"},status=status.HTTP_204_NO_CONTENT)

