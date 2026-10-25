from django.db import models

from apps.products.models import Product
from apps.users.models import User


class Order(models.Model):
    """订单主表"""
    STATUS_CHOICES = (
        (0, '待支付'),
        (1, '已支付'),
        (2, '已发货'),
        (3, '已完成'),
        (4, '已取消'),
    )
    order_no = models.CharField('订单号', max_length=32, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', verbose_name='用户')
    status = models.SmallIntegerField('状态', default=0, choices=STATUS_CHOICES)
    total_amount = models.DecimalField('总金额', max_digits=10, decimal_places=2)
    pay_type = models.CharField('支付方式', max_length=20, default='mock')
    receiver_name = models.CharField('收货人', max_length=50, blank=True, default='')
    receiver_phone = models.CharField('收货电话', max_length=20, blank=True, default='')
    receiver_address = models.CharField('收货地址', max_length=300, blank=True, default='')
    remark = models.CharField('备注', max_length=300, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(null=True, blank=True)
    ship_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'mall_order'
        ordering = ['-id']
        verbose_name = '订单'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_no


class OrderItem(models.Model):
    """订单明细（商品快照，防止商品信息变更影响历史订单）"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='订单')
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='商品')
    title = models.CharField('商品名', max_length=200)
    cover = models.CharField('封面', max_length=500, blank=True, default='')
    price = models.DecimalField('成交价', max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField('数量', default=1)

    class Meta:
        db_table = 'mall_order_item'
        verbose_name = '订单明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.order.order_no}-{self.title}'
