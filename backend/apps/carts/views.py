from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product

from .models import CartItem
from .serializers import CartItemSerializer


class CartView(APIView):
    """购物车：查询 / 加入商品"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        items = CartItem.objects.filter(user=request.user) \
            .select_related('product').order_by('-created_at')
        data = CartItemSerializer(items, many=True).data
        selected = [i for i in data if i['selected']]
        total = round(sum(float(i['subtotal']) for i in selected), 2)
        return Response({
            'items': data,
            'count': items.count(),
            'selected_count': len(selected),
            'total': total,
        })

    def post(self, request):
        product = get_object_or_404(Product, pk=request.data.get('product_id'), status=1)
        quantity = max(1, min(int(request.data.get('quantity', 1)), product.stock))
        item, created = CartItem.objects.get_or_create(
            user=request.user, product=product, defaults={'quantity': quantity})
        if not created:
            item.quantity = min(item.quantity + quantity, product.stock)
            item.save(update_fields=['quantity'])
        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemView(APIView):
    """购物车条目：改数量 / 勾选 / 删除"""
    permission_classes = [permissions.IsAuthenticated]

    def _get(self, request, pk):
        return get_object_or_404(CartItem, pk=pk, user=request.user)

    def patch(self, request, pk):
        item = self._get(request, pk)
        if 'quantity' in request.data:
            item.quantity = max(1, min(int(request.data['quantity']), item.product.stock))
        if 'selected' in request.data:
            item.selected = bool(request.data['selected'])
        item.save()
        return Response(CartItemSerializer(item).data)

    def delete(self, request, pk):
        self._get(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartSelectAllView(APIView):
    """全选 / 全不选"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        selected = bool(request.data.get('selected', True))
        CartItem.objects.filter(user=request.user).update(selected=selected)
        return Response({'ok': True})
