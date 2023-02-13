from django.urls import path
from . import views 

urlpatterns = [
    path('category', views.CategoryAPIView.as_view(), name='api-category'),
    path('product/list', views.ProductAPIView.as_view(), name="product-list"),
    path('catgory/products', views.ProductCategoryAPIView.as_view(), name='products-category'),
    path('product/<int:pk>', views.ProductDetailAPIView.as_view(), name='product-detail'), 
    path('consumer', views.UserAPIView.as_view(), name="consumer-info"),
    path('accounts/register', views.RegistrationView.as_view(), name='register'),  
]
