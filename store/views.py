from django.shortcuts import render
from .models import Product, Category, Consumer, Cart, OrderedItem
from .serializer import CategorySerializer, ProductInfoSerializer, ConsumerInfoSerializer, RegistrationSerializer,VendorSerializer
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from .pagination import CustomPagination
from django.db.models import Q
from rest_framework.decorators import api_view
from .utils import get_tokens_for_user
from admins.models import User
from rest_framework import status
from collections import namedtuple
# Create your views here.
@api_view(['GET', 'POST'])
def api_user(request):
    if request.user.is_authenticated:
        consumer = Consumer.objects.get_or_create(user=request.user)
        instance = ConsumerInfoSerializer(consumer).data
        if request.method == 'POST':
           
                cart.save()
        return Response(instance)

class UserAPIView(APIView):

    def get(self, reuqest):
        queryset,created = Consumer.objects.get_or_create(user=self.request.user)
        serializer = ConsumerInfoSerializer(queryset).data
        return Response(serializer)
    
    def post(self, request):
        action = request.data.get('action')
        id = request.data.get('product')
        consumer, created = Consumer.objects.get_or_create(user=self.request.user)
        cart,created = Cart.objects.get_or_create(consumer = consumer, processing=False, completed=False)
        if action== 'cart':
            product = Product.objects.get(id=id)
            updated, created = OrderedItem.objects.get_or_create(item=product, processing=False, consumer=consumer)
            if updated in cart.items.filter(item=updated.item):
                cart.items.remove(updated)
                updated.delete()
                instance = 'false'
            else:
                cart.items.add(updated)
                instance = ProductInfoSerializer(product).data
                instance['quantity'] = 1
        if action == 'loggin':
            for item in request.data.get('cart'):
                product = Product.objects.get(id=item['id'])
                updated, created = OrderedItem.objects.get_or_create(item=product, processing=False, consumer=consumer)
                updated.quantity = item['quantity']
                updated.save()
                print(updated.quantity, updated.item.name, updated)    
                if updated not in cart.items.filter(item=updated.item):
                    cart.items.add(updated)
                    
            instance = ConsumerInfoSerializer(Consumer.objects.get(user=self.request.user)).data
        
        return Response(instance)
        
        
class CategoryAPIView(ListCreateAPIView):
    queryset = Category.objects.all().filter(parent=None)
    serializer_class = CategorySerializer

class ProductAPIView(ListAPIView):
    serializer_class = ProductInfoSerializer
    pagination_class = CustomPagination
    
    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset
    
    def post(self, request):
        # get search input from request
        category = request.data.get('category', "")
        name = request.data.get('name', "")
        range = request.data.get('range', (0, float('inf')))
        print(range)
        paginator = CustomPagination()
        
        # filter queryset for matching products to search
        queryset = Product.objects.filter(Q(name__icontains=name) & Q(category__title__icontains=category) & Q(price__range=range))
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class ProductCategoryAPIView(APIView):
    def get(self, request):
        products = {}
        for category in Category.objects.all():
            products.setdefault(category.head(), [])
            for product in Product.objects.filter(category=category):
                serializer = ProductInfoSerializer(product).data
                products[category.head()].append(serializer)
        products = dict(sorted(products.items(), key=lambda item: len(item[1]), reverse=True))
        return Response(products)    
    
    
class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer

            
class ConsumserInfoAPIView(RetrieveAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerInfoSerializer    
        

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email = serializer.data['email'])
            auth_data = get_tokens_for_user(user)
            return Response({**auth_data})
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response('true')
        

class ProductClassAPIView(APIView):
    def get(self,request, pk):
        data = {}
        item = Product.objects.get(id=pk)
        product = ProductInfoSerializer(item).data
        owner = VendorSerializer(item.owner).data
        data['product'] = product
        data['owner'] = owner
        return Response(data)
