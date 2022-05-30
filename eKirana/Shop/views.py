from .serializers import ShopInventorySerializer, ShopSerializer,InventorySummarySerializer ,get_Userid,getUserType,getShop
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status,generics
from rest_framework.response import Response
from .models import Shopkeeper, Shop_OrderInventory
from rest_framework.views import APIView
from .pagination import CustomPagination


class ShopAPIView(generics.GenericAPIView):
    queryset = Shopkeeper.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['Shop_Name', 'Locality','State','Pincode']
    ordering_fields = ['State','Locality']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self,request,pk=None):
        id=pk
        if id is not None:
            if Shopkeeper.objects.filter(id=id).exists():
                shop = Shopkeeper.objects.get(id=id)
                serializer = ShopSerializer(shop)
                return Response(serializer.data,status=status.HTTP_200_OK )
            return Response({"Error":"No Shop with matching ID"},status=status.HTTP_400_BAD_REQUEST)
        shop = self.filter_queryset(Shopkeeper.objects.all())
        serializer = ShopSerializer(shop,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK )

    def post(self,request,*args, **kwargs):
        
        serializer  = ShopSerializer(data=request.data,context={ 'request': self.request })
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message":"Shop Registerd Successfully",
                    "Shopname":serializer.data['Shop_Name']
                },status=status.HTTP_201_CREATED
            )
        return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

class ShopInventoryAPIView(generics.GenericAPIView):
    queryset = Shop_OrderInventory.objects.all()
    serializer_class = InventorySummarySerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,pk=None):
        id=pk
        uid = get_Userid(request)
        utype = getUserType(uid)
        if utype == 0:
            return Response({"Message":"User is Not Seller"},status=status.HTTP_200_OK )
        shop = getShop(uid)
        if id is not None:
            if Shop_OrderInventory.objects.filter(Seller=shop,id=id).exists():
                orderitems = Shop_OrderInventory.objects.filter(Seller=shop,id=id)
                serializer = ShopInventorySerializer(orderitems,many=True)
                return Response(
                                {
                                    "order details": serializer.data,
                                },status=status.HTTP_200_OK 
                            )
            return Response(
                                {
                                    "error": "No order found",
                                },status=status.HTTP_200_OK 
                            )
        order = Shop_OrderInventory.objects.filter(Seller=shop)
        print(order)
        filter_backends = self.filter_queryset(order)
        serializer = InventorySummarySerializer(order,many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
        # return Response(
        #     {
        #         "orders": serializer.data,
        #     },status=status.HTTP_200_OK 
        # )