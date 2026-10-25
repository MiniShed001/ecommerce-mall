"""Redis 缓存服务：首页聚合 / 商品详情 两级缓存"""
from django.core.cache import cache

from .models import Category, Product
from .serializers import CategorySerializer, ProductDetailSerializer, ProductListSerializer

HOME_CACHE_KEY = 'mall:home:v1'
PRODUCT_CACHE_KEY = 'mall:product:{pk}'
HOME_TTL = 300        # 首页缓存 5 分钟
PRODUCT_TTL = 600     # 商品详情缓存 10 分钟


def get_home_data():
    """首页聚合数据（banners/热门/新品/分类），优先命中 Redis"""
    data = cache.get(HOME_CACHE_KEY)
    if data is not None:
        return data

    banners = [{'id': p.id, 'image': p.cover, 'title': p.name}
               for p in Product.objects.filter(status=1, is_hot=True)[:4]]
    hot = ProductListSerializer(
        Product.objects.filter(status=1, is_hot=True)[:6], many=True).data
    news = ProductListSerializer(
        Product.objects.filter(status=1, is_new=True)[:8], many=True).data
    categories = CategorySerializer(
        Category.objects.filter(parent__isnull=True), many=True).data

    data = {'banners': banners, 'hot': hot, 'new': news, 'categories': categories}
    cache.set(HOME_CACHE_KEY, data, HOME_TTL)
    return data


def get_product_detail(pk):
    """商品详情，优先命中 Redis"""
    key = PRODUCT_CACHE_KEY.format(pk=pk)
    data = cache.get(key)
    if data is not None:
        return data
    try:
        product = Product.objects.select_related('category').get(pk=pk, status=1)
    except Product.DoesNotExist:
        return None
    data = ProductDetailSerializer(product).data
    cache.set(key, data, PRODUCT_TTL)
    return data


def invalidate_product_cache(pk=None):
    """商品变更时清理相关缓存，保证数据一致性"""
    cache.delete(HOME_CACHE_KEY)
    if pk:
        cache.delete(PRODUCT_CACHE_KEY.format(pk=pk))
