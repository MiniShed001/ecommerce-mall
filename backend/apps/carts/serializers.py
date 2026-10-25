from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    title = serializers.CharField(source='product.name', read_only=True)
    cover = serializers.CharField(source='product.cover', read_only=True)
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    stock = serializers.IntegerField(source='product.stock', read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'title', 'cover', 'price', 'stock',
                  'quantity', 'selected', 'subtotal', 'created_at']

    def get_subtotal(self, obj):
        return str(obj.product.price * obj.quantity)
