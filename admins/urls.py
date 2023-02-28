from django.urls import path
from . import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name='admin-index'),
    path('add-product', views.ProductCreateView.as_view(), name='add-product'),
]