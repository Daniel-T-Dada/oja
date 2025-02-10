from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session

        # Get request
        self.request = request

        # Get request
        self.request = request

        # Get the current session key if it exists
        cart = self.session.get('session_key')

        # if the user is new, no session key! Create one!
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        # Make sure cart is availabel on all pages of site
        self.cart = cart
    

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
            # self.cart[product_id] += int(product_qty)
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # 
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))



    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        # Logic
        if product_id in self.cart:
            pass
            # self.cart[product_id] += int(product_qty)
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # 
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))


    def cart_total(self):
        # Get product IDs
        product_ids = self.cart.keys()

        # lookup those keys in our products database model
        products = Product.objects.filter(id__in=product_ids)

        # Get quantities
        quantities = self.cart

        # print("Cart contents:", quantities)

        # Counting from 0
        total = 0
        for key, value in quantities.items():
            # Convert key string into int so we can do maths calculations on them
            key = int(key)
            for product in products:
                if product.id == key:
                    # print(f"Calculating total for product ID: {product.id}, Quantity: {value}, Price: {product.price}, Sale Price: {product.sale_price}")
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        # print("Total cart value:", total)
        return total

    def __len__(self):
        return len(self.cart)

    def get_prods(self):
        # Get ids from cart
        product_ids = self.cart.keys()

        # Use ids to lookup products in db
        products = Product.objects.filter(id__in=product_ids)

        # Return looked up products
        return products

    def get_quants(self):
        quantities = {str(k): v for k, v in self.cart.items()}
        return quantities

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # Get cart
        ourcart = self.cart

        # Update Dictionary/cart - Our cart is a dictionary
        ourcart[product_id] = product_qty

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # 
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

        thing = self.cart
        return thing

    def delete(self, product):
        product_id = str(product)

        # Delete from Dictionary/Cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # 
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
            # Save carty to the Profile Model
            current_user.update(old_cart=str(carty))
