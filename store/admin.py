from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Category)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display']
    

admin.site.register(Product, ProductAdmin)
admin.site.register(Consumer)
admin.site.register(Cart)
admin.site.register(OrderedItem)
