from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'title', 'price', 'quantity')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_no', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status',)
    search_fields = ('order_no', 'receiver_name', 'receiver_phone')
    inlines = [OrderItemInline]
