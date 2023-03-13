import datetime
import json
import os

import cloudinary
import httpx
from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from textblob import TextBlob

from admins.models import User, Vendor
from .models import Product, Category, Consumer, Cart, Review

images_dir = os.path.join(settings.BASE_DIR, 'static/web/images/shop')
images_list = os.listdir(images_dir)
f = open(os.path.join(settings.BASE_DIR, 'category-icon.json'))
icons = json.load(f)


class CategoryInfoSerializer(serializers.RelatedField):
    def to_representation(self, value):
        return value.head()


class ReviewDetailSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%H:%m:%d')

    class Meta:
        model = Review
        fields = [
            'user', 'content', 'timestamp', 'reply', 'review_percent'
        ]


class ProductSerializer(serializers.Serializer):
    name = serializers.CharField(validators=[UniqueValidator(queryset=Vendor.objects.all())])
    price = serializers.CharField()

    category = serializers.CharField()
    discount = serializers.FloatField(required=False)
    description = serializers.CharField()
    brand = serializers.CharField(required=False)
    available = serializers.IntegerField(required=False)
    discount_duration = serializers.DateTimeField(required=False)

    def validate_name(self, value):
        name = TextBlob(value)
        return name.title().correct()

    def validate_description(self, value):
        if len(value) < 20:
            raise serializers.ValidationError('description should contain at least characters')
        return value

    def validate_category(self, value):
        return Category.objects.get(id=value)

    def validate_price(self, value):
        num = value.split('$')
        try:
            price = float(num[1])
            if price > 10:
                return price
            raise serializers.ValidationError('this is not a charity website!!')
        except ValueError or TypeError:
            raise serializers.ValidationError('valid amount is required')

    def validate_discount_duration(self, value):
        if value < datetime.datetime.now:
            return serializers.ValidationError('discount duration cannot be in past')

    def create(self, validated_data):
        for product in Product.objects.filter(owner=validated_data['owner']):
            if validated_data['name'] == product.name:
                return serializers.ValidationError('product cannot have same name for vendor')
        validated_data['Brand'] = validated_data.get('brand')
        del validated_data['brand']
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.Brand = validated_data.get('brand', instance.Brand)
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.description = validated_data.get('description', instance.description)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance


class ProductInfoSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    image = serializers.SerializerMethodField()
    discount_price = serializers.SerializerMethodField()
    category = CategoryInfoSerializer(read_only=True)
    discount_duration = serializers.DateTimeField(format='%Y, %m, %d')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'image', 'description', 'discount', 'category', 'available', 'discount_price',
            'discount_duration', 'review_percentage', 'review_average', 'review_count'
        ]

    def get_image(self, obj):
        v_image = images_list[(obj.id % 21)]
        if not obj.images.all():
            return [f'/static/web/images/shop/{v_image}'] * 2
        else:
            try:

                return [cloudinary.CloudinaryImage(x.image.public_id).build_url(width=800,
                                                                                height=900,
                                                                                crop='fill',
                                                                                responsive=True) for x in
                        obj.images.all()]
            except httpx.ConnectError:
                return [f'/static/web/images/shop/{v_image}'] * 2

    def get_discount_price(self, obj):
        if obj.discount:
            return obj.price - ((obj.discount / 100) * obj.price)


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
        fields = [
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
            'user', 'wish_list', 'cart'
        ]

    def get_cart(self, obj):
        data = []
        cart, created = Cart.objects.get_or_create(consumer=obj, processing=False, completed=False)
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
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = [
            'email', 'password2', 'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
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
