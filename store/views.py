import json
import os

import cloudinary
import httpx
import rest_framework_simplejwt.authentication
from django.conf import settings
from django.db.models import Q
from django.template.loader import render_to_string
from dotenv import load_dotenv
from pyuploadcare import Uploadcare
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from admins.models import User, Vendor
from .models import Product, Category, Consumer, Cart, OrderedItem, Review
from .pagination import CustomPagination
from .permissions import CustomPermission
from .serializer import CategorySerializer, ProductInfoSerializer, ConsumerInfoSerializer, RegistrationSerializer, \
    ProductSerializer
from .utils import get_tokens_for_user, upload_image

load_dotenv()

uploadcare = Uploadcare(public_key=str(os.getenv('public_key')), secret_key=str(os.getenv('secret')))


# Create your views here.
class UserAPIView(APIView):
    # TODO: add quick serializer
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
        if action == 'wishlist':
            product = Product.objects.get(pk=pk)
            if product in consumer.wish_list.all():
                consumer.wish_list.remove(product)
            else:
                consumer.wish_list.add(product)
                instance = True
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
        print(self.request.query_params)
        # get search input from request
        name = request.data.get('name', "")
        category = request.data.get('category', "")
        price = [request.data.get('min_price'), request.data.get('max_price')]
        paginator = CustomPagination()

        # filter queryset for matching products to search
        queryset = Product.objects.filter(
            Q(name__icontains=name) & Q(category__title__icontains=category) & Q(price__range=price))
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CategoryProductAPIView(ListAPIView):
    serializer_class = ProductInfoSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = [product for product in Product.objects.all() if
                    product.category.head() == self.kwargs.get('category')]
        return queryset

    def post(self, request, category):
        # get search input from request
        name = request.data.get('name', "")
        price = range(request.data.get('min_price'), request.data.get('max_price'))
        paginator = CustomPagination()
        # filter queryset for matching products to search
        queryset = [product for product in Product.objects.filter(name__icontains=name) if (
                product.product_discount() in price or product.price in price)
                    and product.category.head() == self.kwargs.get(
            'category')]

        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductInfoSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class CategoryItemAPIView(APIView):
    def get(self, request):
        products = {}
        for category in Category.objects.all():
            products.setdefault(category.head(), [])
            for product in Product.objects.filter(category=category):
                serializer = ProductInfoSerializer(product).data
                products[category.head()].append(serializer)
        products = dict(sorted(products.items(), key=lambda item: len(item[1]), reverse=True))
        return Response(products)


class ReviewAPIView(APIView):
    authentication_classes = [rest_framework_simplejwt.authentication.JWTAuthentication]
    permission_classes = [CustomPermission]

    def post(self, request):
        rating = request.data.get('rating')
        content = request.data.get('content')
        if request.data.get('post'):
            item = Product.objects.get(pk=request.data.get('post'))
            Review.objects.create(post=Product.objects.get(id=request.data.get('post')), user=request.user,
                                  rating=rating,
                                  content=content)
            product = ProductInfoSerializer(item).data
            reviews = Review.objects.filter(post=item)
            context = {
                'reviews': reviews,
                'product': product
            }
            form = render_to_string('partials/comment-section.html', context, request=request)
            return Response({'form': form, 'product': True})
        else:
            owner = Vendor.objects.get(name=request.data.get('vendor'))
            review = Review.objects.create(vendor=owner, content=content, rating=rating, user=request.user)
            data = {
                'vendor': True
            }
            return Response(data)


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


@api_view(['GET'])
def famous_category(request):
    query = request.GET.get('q')
    with open('famous_brands.json') as file:
        data = json.load(file)
        result = []
        for item in data:
            if query in item['id']:
                result.append(item)
        return Response(result)


class ProductCreateEditAPIView(APIView):

    def get(self, request, pk=None):
        images_dir = os.path.join(settings.BASE_DIR, 'static/web/images/shop')
        images_list = os.listdir(images_dir)
        if pk is not None:
            item = Product.objects.get(id=pk)
            v_image = images_list[(item.id % 21)]
            if not item.images.all():
                return Response([f'/static/web/images/shop/{v_image}'])
            else:
                try:
                    return Response(
                        cloudinary.CloudinaryImage(x.image.public_id).build_url(height=120, width=110, crop='fill') for
                        x in
                        item.images.all())
                except httpx.ConnectError:
                    return Response([f'/static/web/images/shop/{v_image}'])

    def post(self, request, pk=None):
        serializer = ProductSerializer(data=request.data)
        if pk is not None:
            item = Product.objects.get(id=pk)
            serializer = ProductSerializer(data=request.data, instance=item)
        if request.data.get('file') and pk is not None:
            file = request.data.get('file')
            photo = upload_image(file)

            if item:
                item.images.add(photo)
            return Response(True)
        else:
            if serializer.is_valid():
                if pk is None:
                    serializer.validated_data['owner'] = Vendor.objects.get(owner=request.user)
                serializer.save()
                return Response(True)
            return Response(serializer.errors)


product_update = ProductCreateEditAPIView()
