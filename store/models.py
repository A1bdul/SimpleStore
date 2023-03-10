import os
import uuid

import httpx
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from tinymce import models as tinymce_models

from admins.models import Vendor, User

images_dir = os.path.join(settings.BASE_DIR, 'static/web/images/shop')
images_list = os.listdir(images_dir)


def validate_price(value):
    if value <= 0:
        raise ValidationError(
            _("%(value)s is not valid price for product"), params={'value': value})


def validate_description(value):
    if len(value) <= 20:
        raise ValidationError(
            _("%(value)s is not valid price for product"), params={'value': value})


# Create your models here.


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wish_list = models.ManyToManyField('Product', blank=True)

    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=20)
    mobile_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=200)
    zip = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.email


class Images(models.Model):
    from cloudinary.models import CloudinaryField

    image = CloudinaryField()


class Product(PolymorphicModel):
    name = models.CharField(max_length=200)

    images = models.ManyToManyField(Images, related_name='images', blank=True)
    description = tinymce_models.HTMLField(validators=[validate_description])
    available = models.IntegerField(null=True, blank=True)
    price = models.FloatField(validators=[validate_price])
    discount = models.FloatField(blank=True, null=True)
    discount_duration = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    Brand = models.CharField(max_length=200, blank=True, null=True)
    attribute = models.ManyToManyField('Attribute', blank=True)
    owner = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    class Meta:
        ordering = ('-id',)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save()

    def __str__(self):
        return f"{self.name}"

    @admin.display(description="")
    def image_display(self):

        v_image = images_list[(self.id % 21)]
        if not self.images.all():
            v_image = f'/static/web/images/shop/{v_image}'
        else:
            try:
                image = self.images.last()
                v_image = image.image.url
                print(image.image)
            except httpx.ConnectError:
                v_image = f'/static/web/images/shop/{v_image}'
        return format_html(
            '<img src="{}" width="30" alt="{}"> ', v_image, self.name
        )

    @admin.display(description="Price")
    def price_display(self):
        return '$' + str(self.price)

    def product_discount(self):
        if self.discount:
            return self.price - ((self.discount / 100) * self.price)

    def review_percentage(self):
        rating = 0
        reviews = Review.objects.filter(post=self)
        if reviews:
            for review in reviews:
                rating += review.rating
            return (rating / (Review.objects.filter(post=self).count() * 5)) * 100
        return 0

    def review_average(self):
        rating = 0
        reviews = Review.objects.filter(post=self)
        if reviews:
            for review in reviews:
                rating += review.rating
            return rating / (Review.objects.filter(post=self).count())
        return 0

    def review_count(self):
        return Review.objects.filter(post=self).count()


class Attribute(models.Model):
    value = models.CharField(max_length=500)


def category_sort(n):
    return n.children.count()


class Category(PolymorphicModel):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.FileField(
        null=True, blank=True
    )
    order = models.IntegerField(default=0)
    slug = models.SlugField(max_length=225, verbose_name=f'Brand slug', editable=False)
    thumbnail_width = models.IntegerField(blank=True, null=True)
    thumbnail_height = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(default=now)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ('order', 'title')

    def __str__(self):

        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return '->'.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if self.thumbnail:
            from django.core.files.images import get_image_dimensions
            import django
            if django.VERSION[1] < 2:
                width, height = get_image_dimensions(self.thumbnail.file)
            else:
                width, height = get_image_dimensions(self.thumbnail.file, close=True)
        else:
            width, height = None, None
        if self.parent is not None:
            self.order = 0
        self.thumbnail_width = width
        self.thumbnail_height = height
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

        parents = sorted(Category.objects.filter(parent=None), key=category_sort, reverse=True)
        for index, category in enumerate(parents, start=1):

            if category.order != index:
                category.order = index
                category.save()

    def head(self):
        if self.parent is None:
            return self.title
        else:
            k = self.parent
            while k.parent is not None:
                k = k.parent
                print(k)

            return k.title

    def category_list(self):
        categories = []
        it = iter(self.children.all())
        for x, y in zip(it, it):
            i = [x.title, y.title]
            categories.append(i)
        if categories:
            return categories
        return None


class OrderedItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ordered_item')
    quantity = models.IntegerField(default=1)
    processing = models.BooleanField(default=False)
    consumer = models.ForeignKey(Consumer, on_delete=models.SET_NULL, null=True)

    def ordered_item_total(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name + '->' + str(self.quantity)


class Cart(models.Model):
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True)

    items = models.ManyToManyField(OrderedItem, blank=True)
    transaction_id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    completed = models.BooleanField(default=False)
    date_ordered = models.DateTimeField(auto_now_add=True)
    processing = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    def vendor_cart(self, vendor):
        cart = {
            'consumer': self.consumer,
            'id': '%s' % self.transaction_id,
            'date_ordered': self.date_ordered
        }
        price = 0
        for item in self.items.all():
            if item.item.owner == vendor:
                price += item.item.price
        cart['price'] = price
        return cart

    def cart_total(self):
        total = sum([price.ordered_item_total() for price in self.items.all()])
        return total

    def quantity_total(self):
        return self.items.count()


def validate_rating(value):
    if value > 5 or value < 1:
        raise ValidationError(_('%(value)s is invalid rating'), params={'value': value})


class Review(models.Model):
    post = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    vendor = models.ForeignKey(Vendor, related_name='review', on_delete=models.CASCADE, blank=True, null=True)
    reply = models.ForeignKey('Review', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    content = models.TextField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(validators=[validate_rating], null=True)

    def review_percent(self):
        return (self.rating / 5) * 100
