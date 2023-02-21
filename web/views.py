from django.shortcuts import render
from django.views import View
# Create your views here.

class HomeView(View):
    template_name = 'web/index.html'
    def get(self, request):
        return render(request,self.template_name)

class ShopView(View):
    template_name = 'web/shop.html'
    def get(self, request):
        return render(request,self.template_name)

class CheckOutView(View):
    template_name = 'web/checkout.html'
    def get(self, request):
        return render(request,self.template_name)
    
class CompareView(View):
    template_name = 'web/compare.html'
    def get(self, request):
        return render(request,self.template_name)
    
class CartView(View):
    template_name = 'web/cart.html'
    def get(self, request):
        return render(request,self.template_name)
    
class OrderView(View):
    template_name = 'web/order-view.html'
    def get(self, request):
        return render(request,self.template_name)

class WishListView(View):
    template_name = 'web/wishlist.html'
    def get(self, request):
        return render(request,self.template_name)

class AccountView(View):
    template_name = 'web/my-account.html'
    def get(self, request):
        return render(request, self.template_name)


class ProductDetail(View):
    template_name = 'web/product-swatch.html'
    def get(self, request, id):
        return render(request, self.template_name)
