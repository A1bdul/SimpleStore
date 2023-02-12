from django.urls import path
from . import views 

urlpatterns = [
    path('', views.HomeView.as_view(), name='admin-index'),
    path('', views.ProductCreateView.as_view(), name='add-product'),
]
