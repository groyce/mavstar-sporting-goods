from .cart import Cart

# context processor to set the current cart into the request context
def cart(request):
    return {'cart': Cart(request)}