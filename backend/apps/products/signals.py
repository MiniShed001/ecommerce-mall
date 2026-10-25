from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Product
from .services import invalidate_product_cache


@receiver([post_save, post_delete], sender=Product)
def on_product_change(sender, instance, **kwargs):
    """商品新增/修改/删除 -> 自动失效首页与详情缓存"""
    invalidate_product_cache(instance.pk if instance else None)
