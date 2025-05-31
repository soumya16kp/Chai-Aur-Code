from django.urls import path
from .import views

urlpatterns = [
    path('',views.cart_view,name='cart'),
    path('add/', views.add_to_cart, name='add_to_cart'),
    path('update/', views.update_cart, name='update_cart'),
    path('checkout/',views.checkout,name='checkout'),
    path('cart-quantity/', views.cart_quantity, name='cart_quantity'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]
