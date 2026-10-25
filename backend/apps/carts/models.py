from django.db import models

from apps.products.models import Product
from apps.users.models import User


class CartItem(models.Model):
    """购物车条目"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField('数量', default=1)
    selected = models.BooleanField('是否勾选', default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mall_cart_item'
        unique_together = ('user', 'product')
        verbose_name = '购物车'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.user_id}-{self.product_id}'
