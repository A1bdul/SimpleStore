import os
import json
import random
from admins.models import User
from rest_framework import serializers
from .models import Product, Category, Consumer, Cart
from django.conf import settings

images_dir = "C:\\Users\\Laptop\\Desktop\\Abdul's projects\\Wolmart\\static\\web\\images\\shop"
images_list = os.listdir(images_dir)
f = open(os.path.join(settings.BASE_DIR, 'category-icon.json'))
icons = json.load(f)


class CategoryInfoSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.head()


class ProductInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    image = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    category = CategoryInfoSerializer(read_only=True)
    discount_duration = serializers.DateTimeField(format='%Y, %m, %d')
    
    class Meta:
        model = Product
        fields = [
            'id','name','price', 'image', 'discount', 'description', 'category', 'available', 'discount_price', 'discount_duration'
        ]

    def get_image(self, obj):
       if not obj.image:
           return [images_list[(obj.id%21)]]*2
    
    def get_discount_price(self, obj):
        if obj.discount:
            return obj.price - ((obj.discount/100) * obj.price)
        

class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'title', 'category_list', 'head', 'icon'
        ]
        
    def get_icon(self, obj):
        return icons.get(obj.title)
    
    
class UserInfoSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields =[
            'first_name', 'last_name', 'full_name'
        ]
        
    def get_full_name(self, obj):
        return obj.get_full_name()

class ConsumerInfoSerializer(serializers.ModelSerializer):
    user = UserInfoSerializer()
    wish_list = ProductInfoSerializer(many=True)
    cart = serializers.SerializerMethodField()
    
    class Meta:
        model = Consumer
        fields = [
            'user','wish_list', 'cart'
        ]

    def get_cart(self, obj):
        data = []
        cart, created = Cart.objects.get_or_create(consumer=obj, completed=False)
        for product in cart.items.all():
            serializer = ProductInfoSerializer(product.item).data
            serializer['quantity'] = product.quantity
            data.append(serializer)
        return data
            
