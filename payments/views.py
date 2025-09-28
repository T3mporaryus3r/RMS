import json
import requests
import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Import models
from orders.models import Order, OrderItem
from food.models import Food   # adjust if you also want drinks


def save_order_from_cart(request, transaction_id, payment_method):
    """
    Save the current session cart into Order + OrderItems.
    """
    cart = request.session.get("cart", {})
    if not cart:
        return None

    total = sum(float(item["price"]) * int(item["quantity"]) for item in cart.values())

    # Create order (link to user if logged in)
    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        transaction_id=transaction_id,
        payment_method=payment_method,
        total_amount=total,
        status="Completed"
    )

    # Save each cart item into OrderItem
    for product_id, item in cart.items():
        try:
            product = Food.objects.get(id=product_id)
        except Food.DoesNotExist:
            continue
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item["quantity"],
            price=item["price"]
        )

    # Clear cart after order is saved
    request.session["cart"] = {}
    request.session.modified = True

    return order


# -------------------------
# Payment Page
# -------------------------
def payment_page(request):
    cart = request.session.get("cart", {})
    total = sum(float(item.get("price", 0)) * int(item.get("quantity", 0)) for item in cart.values())
    return render(request, "payment.html", {
        "total": total,
        "KHALTI_PUBLIC_KEY": settings.KHALTI_PUBLIC_KEY,
        "ESEWA_MERCHANT_ID": settings.ESEWA_MERCHANT_ID,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    })


# -------------------------
# Khalti Verification
# -------------------------
@csrf_exempt
def khalti_verify(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        token = data.get("token")
        amount = int(data.get("amount", 0))  # Khalti expects paisa
    except Exception as e:
        return JsonResponse({"error": "Invalid payload", "details": str(e)}, status=400)

    url = "https://khalti.com/api/v2/payment/verify/"
    payload = {"token": token, "amount": amount}
    headers = {
        "Authorization": f"Key {settings.KHALTI_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    try:
        resp = requests.post(url, json=payload, headers=headers)
        resp_json = resp.json()
    except Exception:
        return JsonResponse({"error": "Khalti request failed"}, status=400)

    if resp.status_code == 200:
        save_order_from_cart(
            request,
            transaction_id=resp_json.get("idx", "KHALTI_TEST"),
            payment_method="Khalti"
        )
        return JsonResponse({"success": True, "data": resp_json})
    return JsonResponse({"success": False, "data": resp_json}, status=400)


# -------------------------
# eSewa Success
# -------------------------
def esewa_success(request):
    txn_uuid = request.GET.get("transaction_uuid")
    amt = request.GET.get("total_amount")
    ref_id = request.GET.get("refId")

    verify_url = "https://rc-epay.esewa.com.np/api/epay/transaction"
    payload = {
        "amount": amt,
        "product_code": settings.ESEWA_MERCHANT_ID,
        "transaction_uuid": txn_uuid,
    }

    try:
        resp = requests.post(verify_url, data=payload, timeout=10)
        if resp.status_code == 200 and "SUCCESS" in resp.text.upper():
            save_order_from_cart(request, transaction_id=txn_uuid, payment_method="eSewa")
            return redirect("my_orders")
        else:
            return HttpResponse("❌ eSewa Verification Failed. Please try again.")
    except Exception as e:
        return HttpResponse(f"⚠️ eSewa Verification Error: {str(e)}")


def esewa_failure(request):
    return HttpResponse("❌ eSewa Payment Failed. Please try again.")


# -------------------------
# Stripe
# -------------------------
@csrf_exempt
def create_checkout_session(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    cart = request.session.get("cart", {})
    total_decimal = sum(float(item.get("price", 0)) * int(item.get("quantity", 0)) for item in cart.values())
    stripe_amount = int(round(total_decimal * 100))  # cents

    stripe.api_key = settings.STRIPE_SECRET_KEY
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": "Food Order"},
                    "unit_amount": stripe_amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=request.build_absolute_uri("/payments/stripe-success/"),
            cancel_url=request.build_absolute_uri("/payments/"),
        )
        return JsonResponse({"url": session.url, "id": session.id})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


def stripe_success(request):
    save_order_from_cart(
        request,
        transaction_id=request.GET.get("session_id", "STRIPE_TEST"),
        payment_method="Stripe"
    )
    return redirect("my_orders")
