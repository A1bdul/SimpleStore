from django.shortcuts import render
from django.views import View
from store.models import OrderedItem

# Create your views here.
class HomeView(View):
    template_name = 'admin/admin.html'
    
    def get(self, request):
        orders = OrderedItem.objects.filter(item__owner=self.request.user)
        return render(request, self.template_name)

class ProductCreateView(View):
    template_name = 'admin/add-product.html'
    
    def get(self, request):
        return render(request, self.template_name)
    