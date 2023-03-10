from rest_framework.permissions import BasePermission, SAFE_METHODS

from admins.models import Vendor
from store.models import Review, Product


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.data.get('post'):
            print(request.data.get('post'))
            item = request.data.get('post')
            return request.user and request.user.is_authenticated and not Review.objects.filter(
                user=request.user, post=Product.objects.get(id=request.data.get('post'))).exists()
        else:
            item = request.data.get('vendor')
            print(item)
            return request.user and request.user.is_authenticated and not Review.objects.filter(
                user=request.user, vendor=Vendor.objects.get(name=item)).exists()
