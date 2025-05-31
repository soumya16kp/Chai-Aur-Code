from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'chai', 'quantity']
    list_filter = ['chai']
    search_fields = ['cart__user__username', 'chai__name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ordered_at', 'status', 'total_amount']
    list_filter = ['status', 'ordered_at']
    search_fields = ['user__username']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'chai', 'quantity', 'price_at_order']
    search_fields = ['order__user__username', 'chai__name']
