import json
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Payment page
def payment_page(request):
    cart = request.session.get("cart", {})
    total = sum(float(item["price"]) * int(item["quantity"]) for item in cart.values())
    khalti_amount = int(total * 100)  # Khalti expects paisa as integer

    return render(request, "payment.html", {
        "total": total,
        "khalti_amount": khalti_amount,
        "KHALTI_PUBLIC_KEY": settings.KHALTI_PUBLIC_KEY,
        "ESEWA_MERCHANT_ID": settings.ESEWA_MERCHANT_ID,
    })

# Khalti Verification
def khalti_verify(request):
    if request.method == "POST":
        data = json.loads(request.body)
        token = data.get("token")
        amount = data.get("amount")  # should be integer paisa

        url = "https://khalti.com/api/v2/payment/verify/"
        payload = {
            "token": token,
            "amount": amount,
        }
        headers = {"Authorization": f"Key {settings.KHALTI_SECRET_KEY}"}

        response = requests.post(url, json=payload, headers=headers)
        resp_dict = response.json()

        if response.status_code == 200:
            request.session["cart"] = {}
            request.session.modified = True
            return JsonResponse({"success": True, "data": resp_dict})
        return JsonResponse({"success": False, "data": resp_dict})

# eSewa Success
def esewa_success(request):
    oid = request.GET.get("oid")
    amt = request.GET.get("amt")
    refId = request.GET.get("refId")

    url = "https://uat.esewa.com.np/epay/transrec"
    payload = {
        "amt": amt,
        "scd": settings.ESEWA_MERCHANT_ID,
        "rid": refId,
        "pid": oid,
    }

    resp = requests.post(url, data=payload)
    if "Success" in resp.text:
        request.session["cart"] = {}
        request.session.modified = True
        return HttpResponse("eSewa Payment Successful")
    return HttpResponse("Payment Verification Failed")

# eSewa Failure
def esewa_failure(request):
    return HttpResponse("eSewa Payment Failed")
