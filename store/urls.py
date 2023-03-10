from django.urls import path

from admins.views import cart_api_view
from . import views

urlpatterns = [
    path('category', views.CategoryAPIView.as_view(), name='api-category'),
    path('products/shop', views.ProductAPIView.as_view(), name="api-product-list"),
    path('product/product-category/<str:category>', views.CategoryProductAPIView.as_view(), name="api-category"),
    path('catgory/products', views.CategoryItemAPIView.as_view(), name='api-products-category'),
    path('product/<int:pk>', views.ProductDetailAPIView.as_view(), name='api-product-detail'),
    path('consumer', views.UserAPIView.as_view(), name="consumer-info"),
    path('accounts/register', views.RegistrationView.as_view(), name='register'),
    path('product-comment', views.ReviewAPIView.as_view(), name="comments"),
    path('cart/<str:pk>', cart_api_view, name="vendor-cart"),
    path('admin/edit-product', views.product_update.as_view(), name="product-update"),
    path('admin/edit-product/<int:pk>', views.product_update.as_view(), name="product-update"),
    path('brands', views.famous_category, name='famous-brands')
]
