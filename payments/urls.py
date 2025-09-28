# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_page, name="payment_page"),
    path("khalti-verify/", views.khalti_verify, name="khalti_verify"),
    path("esewa-success/", views.esewa_success, name="esewa_success"),
    path("esewa-failure/", views.esewa_failure, name="esewa_failure"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),
    path("stripe-success/", views.stripe_success, name="stripe_success"),
]
