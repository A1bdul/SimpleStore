from django.shortcuts import render, get_object_or_404
from django.views import View

from admins.models import Vendor


# Create your views here.
class HomeView(View):
    template_name = 'admin/admin.html'

#    @method_decorator(login_required)
    def get(self, request):
        user = get_object_or_404(Vendor, owner=request.user)
        # orders = OrderedItem.objects.filter(item__owner=self.request.user)
        return render(request, self.template_name, context={'store': user})


class ProductCreateView(View):
    template_name = 'admin/add-product.html'

    def get(self, request):
        return render(request, self.template_name)
