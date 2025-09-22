# Context Processors can reside anywhere in the code ,but having seperate file for them make the code more organized.

from . cart import Cart

def cart(request):
    return {'cart': Cart(request)}