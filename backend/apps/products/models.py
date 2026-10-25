from django.db import models


class Category(models.Model):
    """商品分类（支持两级）"""
    name = models.CharField('分类名', max_length=50)
    parent = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE,
        related_name='children', verbose_name='父分类')
    icon = models.URLField('图标', blank=True, default='')
    sort = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mall_category'
        ordering = ['sort', 'id']
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Product(models.Model):
    """商品"""
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name='products', verbose_name='分类')
    name = models.CharField('商品名', max_length=200)
    subtitle = models.CharField('副标题', max_length=300, blank=True, default='')
    cover = models.URLField('封面图', blank=True, default='')
    gallery = models.JSONField('轮播图', default=list, blank=True)
    price = models.DecimalField('售价', max_digits=10, decimal_places=2)
    original_price = models.DecimalField('原价', max_digits=10, decimal_places=2, default=0)
    stock = models.IntegerField('库存', default=0)
    sales = models.IntegerField('销量', default=0)
    detail = models.TextField('详情', blank=True, default='')
    is_hot = models.BooleanField('热门', default=False)
    is_new = models.BooleanField('新品', default=False)
    status = models.SmallIntegerField('状态', default=1, choices=((1, '上架'), (0, '下架')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mall_product'
        ordering = ['-id']
        verbose_name = '商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
