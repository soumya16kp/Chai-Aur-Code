
import json
from pyexpat.errors import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Cart, CartItem,Order,OrderItem
from chai.models import ChaiVariety
from django.shortcuts import render,get_object_or_404,redirect

def cart_view(request):
    if not request.user.is_authenticated:
        return render(request, 'cart.html', {'cart': None})
    
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(request, 'cart.html', {
        'cart': cart
    })

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    if request.user == item.cart.user:
        item.delete()
    return redirect('cart') 

@csrf_exempt
def add_to_cart(request):
    data = json.loads(request.body)
    chai_id = data.get('chai_id')
    quantity = data.get('quantity')

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    chai = ChaiVariety.objects.get(id=chai_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, chai=chai)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()

    return JsonResponse({'success': True})

@csrf_exempt
def update_cart(request):
    data = json.loads(request.body)
    chai_id = data.get('chai_id')
    quantity = data.get('quantity')

    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Not logged in'})

    try:
        cart = Cart.objects.get(user=request.user)
        item = CartItem.objects.get(cart=cart, chai_id=chai_id)

        if quantity <= 0:
            item.delete()
            return JsonResponse({'success': True, 'message': 'Item removed from cart'})
        else:
            item.quantity = quantity
            item.save()
            return JsonResponse({'success': True, 'message': 'Cart updated'})
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Item not found'})
    except Cart.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cart not found'})



def cart_quantity(request):
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
            return JsonResponse({'total_quantity': cart.total_quantity()})
        except Cart.DoesNotExist:
            return JsonResponse({'total_quantity': 0})
    return JsonResponse({'total_quantity': 0})


def checkout(request):
    try:
        cart=request.user.cart
        cart_items=cart.items.all()

        if not cart_items:
            messages.warning(request,"The cart is empty")
            return redirect('cart')
        if request.method == 'GET':
            cart_items = []
            for item in cart.items.all():
                cart_items.append({
                    'name': item.chai.name,
                    'quantity': item.quantity,
                    'price': item.chai.price,
                    'total': item.total_price()
                })

            total_amount = cart.total_price()

            return render(request, 'confirm.html', {
                'cart_items': cart_items,
                'total_amount': total_amount
            })

        elif request.method == 'POST':
            # Create order
            order = Order.objects.create(user=request.user)

            total_amount = 0
            for item in cart_items:
                price = item.chai.price
                quantity = item.quantity
                OrderItem.objects.create(
                    order=order,
                    chai=item.chai,
                    quantity=quantity,
                    price_at_order=price
                )
                total_amount += price * quantity

            order.total_amount = total_amount
            order.save()

            # Clear the cart
            cart.items.all().delete()

            return render(request, 'success.html', {'order': order})
    

    except Cart.DoesNotExist:
        messages.warning(request, "You don't have a cart yet.")
        return redirect('all_chai') 
        