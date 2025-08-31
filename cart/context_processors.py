def cart_count(request):
    cart = request.session.get('cart', {})
    unique_items = len(cart)  # Number of unique items
    total_quantity = sum(item['quantity'] for item in cart.values())
    return {
        'cart_unique_items': unique_items,
        'cart_total_quantity': total_quantity
    }