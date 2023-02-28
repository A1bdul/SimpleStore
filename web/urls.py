from django.urls import path
from . import views 
from store.views import ProductDetailAPIView
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('checkout', views.CheckOutView.as_view(), name="checkout"),
    path('shop', views.ShopView.as_view(), name="shop"),
    path('order', views.OrderView.as_view(), name="order"),
    path('cart', views.CartView.as_view(), name="cart"),
    path('compare', views.CompareView.as_view(), name="compare"),
    path('product/<int:pk>', views.ProductDetail.as_view(), name="product-detail"),
    path('account', views.AccountView.as_view(), name="account"),
    path('account/wishlist', views.WishListView.as_view(), name="wish_list"),
    path('account/login', views.LoginView.as_view(), name="login"),
    path('account/logout', views.LogoutView.as_view(), name="logout")
]
