from .serializers import ShopSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status,generics
from rest_framework.response import Response
from .models import Shopkeeper



class ShopAPIView(generics.GenericAPIView):
    queryset = Shopkeeper.objects.all()
    serializer_class = ShopSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    search_fields = ['Shop_Name', 'Locality','State','Pincode']
    ordering_fields = ['State','Locality']

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
