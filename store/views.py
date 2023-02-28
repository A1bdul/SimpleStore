import rest_framework_simplejwt.authentication
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from admins.models import User
from .models import Product, Category, Consumer, Cart, OrderedItem, Review
from .pagination import CustomPagination
from .permissions import CustomPermission
from .serializer import CategorySerializer, ProductInfoSerializer, ConsumerInfoSerializer, RegistrationSerializer, \
    VendorSerializer, ReviewDetailSerializer
from .utils import get_tokens_for_user


# Create your views here.
class UserAPIView(APIView):

    def get(self, request):
        queryset, created = Consumer.objects.get_or_create(user=self.request.user)
        serializer = ConsumerInfoSerializer(queryset).data
        return Response(serializer)

    def post(self, request):
        instance = None
        action = request.data.get('action')
        pk = request.data.get('product')
        consumer, created = Consumer.objects.get_or_create(user=self.request.user)
        cart, created = Cart.objects.get_or_create(consumer=consumer, processing=False, completed=False)
        if action == 'cart':
            product = Product.objects.get(pk=pk)
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
                product = Product.objects.get(pk=item['id'])
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
        price = request.data.get('range', (0, float('inf')))
        paginator = CustomPagination()

        # filter queryset for matching products to search
        queryset = Product.objects.filter(
            Q(name__icontains=name) & Q(category__title__icontains=category) & Q(price__range=price))
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


class ReviewAPIView(ListCreateAPIView):
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    permission_classes = [CustomPermission]
    lookup_url_kwarg = 'pk'
    serializer_class = ReviewDetailSerializer

    def get_queryset(self):
        uid = self.kwargs.get(self.lookup_url_kwarg)
        query_set = Review.objects.filter(post=Product.objects.get(id=uid))
        return query_set


class ProductDetailAPIView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductInfoSerializer


class ConsumerInfoAPIView(RetrieveAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerInfoSerializer


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(email=serializer.data['email'])
            auth_data = get_tokens_for_user(user)
            return Response({**auth_data})
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response('true')


class ProductClassAPIView(APIView):
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]

    def get(self, request, pk):
        data = {}
        item = Product.objects.get(pk=pk)
        product = ProductInfoSerializer(item).data
        owner = VendorSerializer(item.owner).data
        owner_items = Product.objects.filter(owner=item.owner).exclude(id=pk)[:5]
        owner_products = ProductInfoSerializer(owner_items, many=True).data
        related_items = Product.objects.filter(category=item.category).exclude(owner=item.owner)[:5]
        related_products = ProductInfoSerializer(related_items, many=True).data

        data['owner'] = owner
        data['product'] = product
        data['vendor_products'] = owner_products
        data['related_products'] = related_products
        return Response(data)
