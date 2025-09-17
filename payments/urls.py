from django.urls import path
from . import views

urlpatterns = [
    path("", views.payment_page, name="payment_page"),
    path("khalti-verify/", views.khalti_verify, name="khalti_verify"),
    path("success/", views.esewa_success, name="esewa_success"),
    path("failure/", views.esewa_failure, name="esewa_failure"),
]
