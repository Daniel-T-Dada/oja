from django.shortcuts import render, get_object_or_404
from .cart import Cart
from store.models import Product
from django.http import JsonResponse

# Create your views here.


def cart_summary(request):
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {'cart_products': cart_products, 'quantities': quantities, 'totals': totals})


def cart_add(request):
    # Get the Cart
    cart = Cart(request)

    # test for POST
    if request.POST.get('action') == 'post':
        # Get the products
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        # lookup product in DB
        product = get_object_or_404(Product, id=product_id)

        # Save to session
        cart.add(product=product, quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()

        # Get updated cart data
        cart_products = cart.get_prods
        quantities = cart.get_quants
        cart_total = cart.cart_total()

        # Return response with cart data
        response = JsonResponse({
            'qty': cart_quantity,
            'cart_total': "{:.2f}".format(cart_total) if cart_total else "0.00",
            'success': True
        })
        return response

    return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # Call delete function in cart
        cart.delete(product=product_id)

        response = JsonResponse({'product': product_id})
        return response


def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))

        cart.update(product=product_id, quantity=product_qty)

        response = JsonResponse({'qty': product_qty})
        return response
