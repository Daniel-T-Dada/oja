from .cart import Cart
from store.models import Product

# Create context processor so our cart can work on all pages of the site
def cart(request):
	cart = Cart(request)
	cart_items = len(cart)
	cart_total = 0
	cart_products = []
	quantities = {}

	if cart_items > 0:
		cart_products = cart.get_prods
		quantities = cart.get_quants
		cart_total = cart.cart_total()

	return {
		'cart': Cart(request),
		'cart_items': cart_items,
		'cart_products': cart_products,
		'cart_total': "{:.2f}".format(cart_total) if cart_total else "0.00",
		'quantities': quantities
	}