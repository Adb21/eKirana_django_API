from django import views
from .serializers import ProductSerializer
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework import status,generics,viewsets
from rest_framework.pagination import PageNumberPagination
from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from .pagination import CustomPagination


# Create your views here.
class ProductListAPIVIew(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    filterset_fields = ['Category','Shop_id']
    search_fields = ['Title', 'Category','Shop_id']
    ordering_fields = ['Title','Category']
    pagination_class = CustomPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        ...
        
        queryset = Product.objects.all()
        filter_backends = self.filter_queryset(queryset)
        serializer = ProductSerializer(filter_backends, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

class ProductRetriveAPIVIew(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductCreateAPIView(generics.GenericAPIView):
    # queryset = Product.objects.all()
    # serializer_class = ProductSerializer
    # filter_backends = [DjangoFilterBackend,SearchFilter,OrderingFilter]
    # filterset_fields = ['Category','Shop_id']
    # search_fields = ['Title', 'Category','Shop_id']
    # ordering_fields = ['Title','Category']

    # def get(self,request,pk=None):
        
    #     id = pk
    #     if id is not None:
    #         if Product.objects.filter(id=id).exists():
    #             product = Product.objects.get(id=id)
    #             serializer = ProductSerializer(product)
    #             return Response(serializer.data,status=status.HTTP_200_OK )
    #         return Response({"Error":"No product with matching ID"},status=status.HTTP_400_BAD_REQUEST)
    #     product = self.filter_queryset(Product.objects.all())
    #     serializer = ProductSerializer(product,many=True)
        
    #     return Response(serializer.data,status=status.HTTP_200_OK )
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        serializer  = ProductSerializer(data=request.data,context={ 'request': self.request })
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "Message":"Added Product Successfully",

                },status=status.HTTP_202_ACCEPTED
            )
        return Response({"Error":serializer.errors},status=status.HTTP_400_BAD_REQUEST)

