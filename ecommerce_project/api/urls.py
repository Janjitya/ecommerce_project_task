from django.urls import path
from . import views
urlpatterns = [
    path('products/', views.ProductListView.as_view(), name="product_list"),
    path('products/create/', views.ProductCreateView.as_view(), name="product_create"),
    path('product/<int:id>/', views.ProductRetrieveUpdateDeleteView.as_view(), name="product_details"),
    path('cart/', views.AddViewCart.as_view(), name='add_view_cart'),
    path('cart/<int:id>/', views.UpdateDeleteCartItemView.as_view(), name="cart_details"),
    path('cart/clear/', views.ClearCartView.as_view(), name='clear_cart'),
    path('cart/total/', views.CartTotalView.as_view(), name="cart_total"),
  
]