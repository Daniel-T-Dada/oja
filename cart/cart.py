from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = getattr(request, 'session', {})
        self.request = request
        cart = self.session.get('session_key', {})
        
        # Make sure cart is available on all pages of site
        self.cart = cart

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if getattr(self.request, 'user', None) and self.request.user.is_authenticated:
            try:
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_user.update(old_cart=str(carty))
            except Exception:
                pass

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass
        else:
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if getattr(self.request, 'user', None) and self.request.user.is_authenticated:
            try:
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_user.update(old_cart=str(carty))
            except Exception:
                pass

    def cart_total(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def get_quants(self):
        quantities = {str(k): v for k, v in self.cart.items()}
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)
        ourcart = self.cart
        ourcart[product_id] = product_qty
        self.session.modified = True

        if getattr(self.request, 'user', None) and self.request.user.is_authenticated:
            try:
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_user.update(old_cart=str(carty))
            except Exception:
                pass

        return self.cart

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True

        if getattr(self.request, 'user', None) and self.request.user.is_authenticated:
            try:
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                current_user.update(old_cart=str(carty))
            except Exception:
                pass
