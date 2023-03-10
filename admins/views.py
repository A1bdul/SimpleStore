import rest_framework.authentication
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response

from admins.forms import ProductForm
from admins.models import Vendor
from store.models import Product, Cart, Category
from store.serializer import ProductInfoSerializer, UserInfoSerializer


# Create your views here.
@login_required()
def home_view(request):
    print(request.user)
    user = get_object_or_404(Vendor, owner=request.user)
    products = Product.objects.filter(owner=user)

    orders = [cart.vendor_cart(user) for cart in set(Cart.objects.filter(processing=True, completed=False,
                                                                         items__item__in=products))]

    return render(request, 'admin/admin.html', context={
        'store': user,
        'products': products[:5],
        'orders': orders
    })


def product_edit(request, id):
    item = get_object_or_404(Product, id=id)
    category = Category.objects.filter(parent=None)
    form = ProductForm(instance=item)
    return render(request, 'admin/add-product.html', context={
        'item': item,
        'form': form,
        'category': category
    })


def admin_products(request):
    products = Product.objects.filter(owner=Vendor.objects.get(owner=request.user))
    context = {
        'products': products
    }
    return render(request, 'admin/product-list.html', context)


class ProductCreateView(View):
    template_name = 'admin/add-product.html'

    def get(self, request, id=None):
        if id is not None:
            print(id)
        category = Category.objects.filter(parent=None)
        print([cat.children.all() for cat in category])
        form = ProductForm()
        return render(request, 'admin/add-product.html', context={
            'form': form,
            'category': category
        })


@api_view(['GET'])
@authentication_classes([rest_framework.authentication.SessionAuthentication])
def cart_api_view(request, pk):
    products = []
    cart = Cart.objects.get(transaction_id=pk)
    user = get_object_or_404(Vendor, owner=request.user)
    for item in cart.items.all():
        if item.item.owner == user:
            product = ProductInfoSerializer(item.item).data
            product['quantity'] = item.quantity
            products.append(product)
    instance = cart.vendor_cart(vendor=user)
    instance['consumer'] = UserInfoSerializer(cart.consumer.user).data
    instance['products'] = products
    return Response(instance)
