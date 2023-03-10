from django.urls import path
from . import views 

urlpatterns = [
    path('', views.home_view, name='admin-index'),
    path('edit-product/<int:id>', views.product_edit, name='edit-product'),
    path('edit-product', views.ProductCreateView.as_view(), name='add-product'),
    path('admin/products', views.admin_products, name='admin-products')
]