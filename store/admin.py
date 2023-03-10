from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)


class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_display', 'name', 'price_display']
    list_filter = ['category', 'owner']


admin.site.register(Product, ProductAdmin)
admin.site.register(Consumer)
admin.site.register(Review)
admin.site.register(Images)
admin.site.register(Cart)
admin.site.register(OrderedItem)
