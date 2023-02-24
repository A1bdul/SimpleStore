import os
import json
import httpx
from admins.models import User, Vendor
from rest_framework import serializers
from .models import Product, Category, Consumer, Cart
from django.conf import settings

images_dir = os.path.join(settings.BASE_DIR, 'static/web/images/shop')
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
        v_image = images_list[(obj.id%21)]
        if not obj.image:
            return [f'/static/web/images/shop/{v_image}']*2
        else:
            try:
                return [x.cdn_url for x in obj.image]
            except httpx.ConnectError:
                return [f'/static/web/images/shop/{v_image}']*2
              

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

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = [
            'email', 'password2', 'password'
        ]    
        extra_kwargs = {
            'password' : {'write_only': True}
        }
        
        
    def save(self):
        user = User(email=self.validated_data['email'])
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        
        user.set_password(password)
        user.save()
        return user
    
class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value