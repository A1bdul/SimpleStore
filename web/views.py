from django.shortcuts import render
from django.views import View

from admins.models import Vendor
from store.models import Product, Review
from store.serializer import ProductInfoSerializer, VendorSerializer


# Create your views here.

class HomeView(View):
    template_name = 'web/index.html'

    def get(self, request):
        return render(request, self.template_name)


class ShopView(View):
    template_name = 'web/shop.html'

    def get(self, request):
        return render(request, self.template_name)


class CheckOutView(View):
    template_name = 'web/checkout.html'

    def get(self, request):
        return render(request, self.template_name)


class CompareView(View):
    template_name = 'web/compare.html'

    def get(self, request):
        return render(request, self.template_name)


class CartView(View):
    template_name = 'web/cart.html'

    def get(self, request):
        return render(request, self.template_name)


class OrderView(View):
    template_name = 'web/order-view.html'

    def get(self, request):
        return render(request, self.template_name)


class WishListView(View):
    template_name = 'web/wishlist.html'

    def get(self, request):
        return render(request, self.template_name)


class AccountView(View):
    template_name = 'web/my-account.html'

    def get(self, request):
        return render(request, self.template_name)


class ProductDetail(View):
    template_name = 'web/product-swatch.html'

    def get(self, request, pk):
        item = Product.objects.get(pk=pk)
        owner = VendorSerializer(item.owner).data
        product = ProductInfoSerializer(item).data
        reviews = Review.objects.filter(post=item)
        owner_items = Product.objects.filter(owner=item.owner).exclude(id=pk)[:5]
        owner_products = ProductInfoSerializer(owner_items, many=True).data
        related_items = Product.objects.filter(category=item.category).exclude(owner=item.owner)[:5]
        related_products = ProductInfoSerializer(related_items, many=True).data
        other_products = ProductInfoSerializer(Product.objects.all()[item.id:], many=True).data
        return render(request, self.template_name, context={
            'product': product,
            'owner': owner,
            'reviews': reviews,
            'other_products': other_products,
            'owner_products': owner_products,
            'related_products': related_products
        })


class LoginView(View):
    template_name = 'web/login.html'

    def get(self, request):
        return render(request, self.template_name)


class VendorListView(View):
    template_name = 'web/vendor-list.html'
    context = {
        'vendors': Vendor.objects.all()
    }

    def get(self, request):
        return render(request, self.template_name, self.context)


class VendorView(View):
    template_name = 'web/vendor-store.html'

    def get(self, request, name):
        vendor = Vendor.objects.get(name=name)
        reviews = Review.objects.filter(vendor=vendor)
        context = {
            'vendor': vendor,
            'reviews': reviews,
            'products': ProductInfoSerializer(Product.objects.filter(owner=vendor), many=True).data
        }
        return render(request, self.template_name, context)


class LogoutView(View):
    template_name = 'web/login.html'

    def get(self, request):
        print(request.META.get['HTTP_COOKIE'])
        return render(request, self.template_name)


def error_404_view(request, exception):
    return render(request, 'admin/404.html')


class CategoryShopView(View):
    def get(self, request, category):
        products = Product.objects.filter(category__title=category)
        return render(request, 'web/shop.html', context={
            'products': products
        })
