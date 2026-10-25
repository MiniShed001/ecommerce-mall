from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product
from .serializers import CategorySerializer, ProductListSerializer
from .services import get_home_data, get_product_detail


class HomeView(APIView):
    """首页聚合数据（走 Redis 缓存）"""

    def get(self, request):
        return Response(get_home_data())


class CategoryListView(APIView):
    """一级分类列表"""

    def get(self, request):
        qs = Category.objects.filter(parent__isnull=True)
        return Response(CategorySerializer(qs, many=True).data)


class ProductListView(APIView):
    """商品列表：支持 category / keyword / hot / new + 分页"""

    def get(self, request):
        qs = Product.objects.filter(status=1).select_related('category')
        cid = request.query_params.get('category')
        kw = request.query_params.get('keyword')
        hot = request.query_params.get('hot')
        new = request.query_params.get('new')
        if cid:
            qs = qs.filter(category_id=cid)
        if kw:
            qs = qs.filter(name__icontains=kw)
        if hot == '1':
            qs = qs.filter(is_hot=True)
        if new == '1':
            qs = qs.filter(is_new=True)

        try:
            page = max(int(request.query_params.get('page', 1)), 1)
            size = min(int(request.query_params.get('page_size', 10)), 50)
        except ValueError:
            page, size = 1, 10

        total = qs.count()
        start = (page - 1) * size
        items = ProductListSerializer(qs[start:start + size], many=True).data
        return Response({'count': total, 'page': page, 'page_size': size, 'results': items})


class ProductDetailView(APIView):
    """商品详情（走 Redis 缓存）"""

    def get(self, request, pk):
        data = get_product_detail(pk)
        if data is None:
            return Response({'detail': '商品不存在或已下架'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data)
