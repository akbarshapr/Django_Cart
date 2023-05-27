from django.urls import path

from .views import CartView, ProductView, add_to_cart, decrease_quantity, delete, increase_quantity

urlpatterns = [
    path('', ProductView.as_view(), name='products'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add_to_cart/<int:pk>/', add_to_cart, name='add_to_cart'),
    path('cart/increase/<int:pk>/', increase_quantity, name='increase_quantity'),
    path('cart/decrease/<int:pk>/', decrease_quantity, name='decrease_quantity'),
    path('cart/delete/<int:pk>/', delete, name='delete'),
]
