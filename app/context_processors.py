from .models import Cart

def cart_item_count(request):
    if request.user.is_authenticated:
        return {'cart_count': sum(item.quantity for item in Cart.objects.filter(user=request.user))}
    return {'cart_count': 0}
