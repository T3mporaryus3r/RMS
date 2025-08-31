from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from food.models import Food
from drinks.models import Drink
import json
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, AnonymousUser
from .models import Cart

@csrf_exempt
def add_to_cart(request, id, item_type='food'):
    if request.method == "POST":
        # Determine if it's food or drink
        if item_type == 'food':
            item = get_object_or_404(Food, id=id)
        else:
            item = get_object_or_404(Drink, id=id)

        # Get the cart from session or create empty dict
        cart = request.session.get("cart", {})

        # Use string key with type prefix to avoid conflicts
        str_id = f"{item_type}_{item.id}"

        if str_id in cart:
            cart[str_id]["quantity"] += 1
        else:
            cart[str_id] = {
                "name": item.name,
                "price": str(item.price),  # Store as string to avoid Decimal issues
                "quantity": 1,
                "type": item_type
            }

        # Save back to session
        request.session["cart"] = cart
        request.session.modified = True
        
        # Calculate counts
        total_quantity = sum(item_data["quantity"] for item_data in cart.values())
        unique_items = len(cart)
        
        request.session["cart_total_quantity"] = total_quantity
        request.session["cart_unique_items"] = unique_items

        return JsonResponse({
            "message": f"{item.name} added to cart!",
            "cart_unique_items": unique_items
        })

    return JsonResponse({"error": "Invalid request"}, status=400)

def update_cart_item(request, id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        str_id = str(id)
        
        if str_id in cart:
            try:
                # Try to get JSON data first
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                    new_quantity = int(data.get('quantity', 1))
                else:
                    # Fallback to form data
                    new_quantity = int(request.POST.get('quantity', 1))
                
                if new_quantity > 0:
                    cart[str_id]["quantity"] = new_quantity
                    request.session["cart"] = cart
                    request.session.modified = True
                    
                    # Update counts
                    unique_items = len(cart)
                    request.session["cart_unique_items"] = unique_items
                    
                    if request.content_type == 'application/json':
                        return JsonResponse({
                            "success": True,
                            "price": cart[str_id]["price"],
                            "unique_items": unique_items
                        })
                    else:
                        return redirect('cart_page')
            except (ValueError, KeyError, json.JSONDecodeError):
                pass
        
        if request.content_type == 'application/json':
            return JsonResponse({"success": False}, status=400)
        else:
            return redirect('cart_page')

def remove_from_cart(request, id):
    if request.method == "POST":
        cart = request.session.get("cart", {})
        str_id = str(id)
        
        if str_id in cart:
            del cart[str_id]
            request.session["cart"] = cart
            request.session.modified = True
            
            # Update counts
            unique_items = len(cart)
            request.session["cart_unique_items"] = unique_items
            
            if request.content_type == 'application/json':
                return JsonResponse({
                    "success": True,
                    "unique_items": unique_items
                })
            else:
                return redirect('cart_page')
        
        if request.content_type == 'application/json':
            return JsonResponse({"success": False}, status=400)
        else:
            return redirect('cart_page')

from decimal import Decimal  # Add this import at the top

def cart_detail(request):
    cart = request.session.get("cart", {})
    cart_items = []
    subtotal = Decimal('0.00')  # Initialize as Decimal

    for item_id, item_data in cart.items():
        # Get the item from database to access image
        image_url = None
        try:
            # Extract type and id from the item_id
            if item_id.startswith('food_'):
                item_db_id = int(item_id.split('_')[1])
                food = Food.objects.get(id=item_db_id)
                image_url = food.image.url if food.image else None
            elif item_id.startswith('drink_'):
                item_db_id = int(item_id.split('_')[1])
                drink = Drink.objects.get(id=item_db_id)
                image_url = drink.image.url if drink.image else None
        except (Food.DoesNotExist, Drink.DoesNotExist, ValueError):
            image_url = None
            
        # Convert price to Decimal for consistent calculations
        price = Decimal(str(item_data["price"]))
        quantity = item_data["quantity"]
        item_total = price * quantity
        
        subtotal += item_total
        
        cart_items.append({
            "id": item_id,
            "name": item_data["name"],
            "price": float(price),  # Convert back to float for template display
            "quantity": quantity,
            "total": float(item_total),  # Convert to float for template
            "image_url": image_url,
            "type": item_data.get("type", "food")
        })

    # Calculate cart summary using Decimal
    tax = round(subtotal * Decimal('0.10'), 2)  # 10% tax
    shipping = Decimal('5.00') if subtotal > 0 else Decimal('0.00')
    total = round(subtotal + tax + shipping, 2)

    # Convert to float for template context (optional, but keeps consistency)
    context = {
        "cart_items": cart_items,
        "subtotal": float(subtotal),
        "tax": float(tax),
        "shipping": float(shipping),
        "total": float(total),
        "unique_items_count": len(cart)
    }
    
    # Update counts in session
    total_quantity = sum(item["quantity"] for item in cart.values())
    unique_items = len(cart)
    request.session["cart_total_quantity"] = total_quantity
    request.session["cart_unique_items"] = unique_items

    return render(request, "cart.html", context)