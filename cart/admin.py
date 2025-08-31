from django.contrib import admin
from .models import Cart

# Simple admin registration without custom options
admin.site.register(Cart)

# Comment out the problematic CartAdmin
# @admin.register(Cart)
# class CartAdmin(admin.ModelAdmin):
#     list_display = ['name', 'item_type', 'price', 'quantity', 'user_session', 'created_at']
#     list_filter = ['item_type', 'created_at']
#     search_fields = ['name', 'user_session']