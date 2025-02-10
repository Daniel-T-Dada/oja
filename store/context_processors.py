def cart_renderer(request):
    # Get cart items from session
    cart = request.session.get('cart', {})
    cart_items = len(cart)
    cart_total = 0
    cart_products = []
    quantities = {}

    if cart_items > 0:
        from .models import Product
        # Get all products in cart
        product_ids = list(cart.keys())
        cart_products = Product.objects.filter(id__in=product_ids)
        
        # Calculate total and store quantities
        for product in cart_products:
            quantity = cart.get(str(product.id))
            quantities[product.id] = quantity
            if product.is_sale:
                cart_total += float(product.sale_price) * quantity
            else:
                cart_total += float(product.price) * quantity

    return {
        'cart_items': cart_items,
        'cart_total': "{:.2f}".format(cart_total),
        'cart_products': cart_products,
        'quantities': quantities
    } 