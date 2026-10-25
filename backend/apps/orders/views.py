import time
import uuid
from decimal import Decimal

from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.carts.models import CartItem
from apps.products.models import Product

from .models import Order, OrderItem
from .serializers import OrderListSerializer


def gen_order_no():
    """订单号：秒级时间戳 + UUID 随机段（8位hex），并发下不碰撞"""
    return time.strftime('%Y%m%d%H%M%S') + uuid.uuid4().hex[:8]


class OrderCreateView(APIView):
    """下单：默认从购物车勾选项结算；也可传 items 直接购买（立即购买）"""
    permission_classes = [permissions.IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        items_data = request.data.get('items')  # [{'product_id': 1, 'quantity': 2}]
        cart_flag = request.data.get('from_cart', True)

        if items_data is None:
            cart_items = list(CartItem.objects.filter(
                user=request.user, selected=True).select_related('product'))
            if not cart_items:
                raise ValidationError({'detail': '购物车没有勾选商品'})
            items_data = [{'product_id': c.product_id, 'quantity': c.quantity} for c in cart_items]

        if not items_data:
            raise ValidationError({'detail': '订单商品不能为空'})

        order = Order.objects.create(
            order_no=gen_order_no(),
            user=request.user,
            total_amount=Decimal('0.00'),  # 先占位，明细汇总后回写
            receiver_name=request.data.get('receiver_name', ''),
            receiver_phone=request.data.get('receiver_phone', ''),
            receiver_address=request.data.get('receiver_address', ''),
            remark=request.data.get('remark', ''),
        )

        total = Decimal('0.00')
        for it in items_data:
            pid = int(it['product_id'])
            qty = int(it['quantity'])
            if qty < 1:
                raise ValidationError({'detail': '购买数量必须大于 0'})
            # 乐观锁原子扣减：库存充足才扣，影响行数=0 即库存不足。
            # 单条 UPDATE 由数据库串行化执行，从根上杜绝超卖，无需依赖行锁。
            updated = Product.objects.filter(pk=pid, status=1, stock__gte=qty).update(
                stock=F('stock') - qty, sales=F('sales') + qty)
            if not updated:
                raise ValidationError({'detail': f'「商品ID {pid}」库存不足'})
            product = Product.objects.get(pk=pid)
            OrderItem.objects.create(
                order=order, product=product, title=product.name,
                cover=product.cover, price=product.price, quantity=qty)
            total += product.price * qty

        order.total_amount = total
        order.save(update_fields=['total_amount'])

        if cart_flag:
            CartItem.objects.filter(user=request.user, selected=True).delete()

        return Response(OrderListSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderListView(APIView):
    """订单列表，可按 status 过滤"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-id')
        st = request.query_params.get('status')
        if st is not None:
            try:
                qs = qs.filter(status=int(st))
            except ValueError:
                pass
        return Response(OrderListSerializer(qs, many=True).data)


class OrderDetailView(APIView):
    """订单详情"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(
            Order.objects.prefetch_related('items'), pk=pk, user=request.user)
        data = OrderListSerializer(order).data
        data.update({
            'receiver_name': order.receiver_name,
            'receiver_phone': order.receiver_phone,
            'receiver_address': order.receiver_address,
            'remark': order.remark,
        })
        return Response(data)


class OrderPayView(APIView):
    """模拟支付：待支付 -> 已支付"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status != 0:
            raise ValidationError({'detail': '订单状态不允许支付'})
        order.status = 1
        order.pay_time = timezone.now()
        order.save(update_fields=['status', 'pay_time'])
        return Response({'detail': '支付成功（模拟）', 'order_no': order.order_no})


class OrderCancelView(APIView):
    """取消订单：回补库存"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        if order.status != 0:
            raise ValidationError({'detail': '订单状态不允许取消'})
        with transaction.atomic():
            for it in order.items.all():
                if it.product_id:
                    Product.objects.filter(pk=it.product_id).update(
                        stock=F('stock') + it.quantity,
                        sales=F('sales') - it.quantity)
            order.status = 4
            order.save(update_fields=['status'])
        return Response({'detail': '订单已取消'})
