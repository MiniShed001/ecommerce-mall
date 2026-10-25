"""初始化电商示例数据：python manage.py seed_data"""
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.products.models import Category, Product

User = get_user_model()


def cover_url(seed):
    return f'https://picsum.photos/seed/mall{seed}/600/600'


# (分类名, [(商品名, 副标题, 售价, 原价, 库存, 热门, 新品), ...])
CATS = {
    '手机数码': [
        ('星曜X10 5G智能手机 12+256GB', '骁龙旗舰芯 · 5000mAh大电池', '2999.00', '3499.00', 200, True, True),
        ('轻薄本 Pro 14 笔记本电脑', '2.8K 90Hz 全面屏 · 16G+512G', '4599.00', '5299.00', 80, True, False),
        ('智能手表 S8 运动版', '血氧监测 · 14天长续航', '899.00', '1199.00', 300, False, True),
    ],
    '家用电器': [
        ('变频冰箱 501L 一级能效', '风冷无霜 · 智能控温', '3299.00', '3999.00', 60, True, False),
        ('静音破壁机 8叶刀头', '一键清洗 · 低噪研磨', '499.00', '699.00', 150, False, True),
        ('空气炸锅 5L 大容量', '360°热风循环 · 无油低脂', '299.00', '399.00', 500, True, False),
    ],
    '服饰鞋包': [
        ('男士立领休闲夹克 春秋款', '轻量防风 · 修身版型', '199.00', '259.00', 400, False, True),
        ('女士慵懒风针织开衫', '软糯亲肤 · 宽松显瘦', '129.00', '169.00', 600, True, False),
        ('缓震透气跑步鞋', '回弹中底 · 轻量透气', '269.00', '329.00', 350, True, True),
    ],
    '美妆个护': [
        ('玻尿酸补水面膜 20片装', '深层补水 · 提亮肤色', '89.00', '129.00', 1000, True, False),
        ('氨基酸温和洗面奶', '敏感肌适用 · 绵密泡沫', '59.00', '79.00', 800, False, True),
        ('清爽防晒霜 SPF50+', '防水防汗 · 不油腻', '79.00', '99.00', 700, False, True),
    ],
    '食品生鲜': [
        ('每日坚果 30包混合装', '独立小包 · 锁鲜营养', '99.00', '129.00', 900, True, False),
        ('新疆灰枣 2斤装', '皮薄肉厚 · 自然晾晒', '39.00', '59.00', 1200, False, True),
        ('冷萃黑咖啡液 10条', '0糖0脂 · 冷热即溶', '69.00', '89.00', 600, True, False),
    ],
    '运动户外': [
        ('加厚防滑折叠瑜伽垫', '8mm加厚 · 回弹护膝', '79.00', '129.00', 450, False, True),
        ('三合一户外冲锋衣', '防风防水 · 抓绒内胆', '399.00', '599.00', 200, True, False),
        ('智能计数跳绳', '精准计数 · 绳体耐磨', '59.00', '99.00', 1000, False, True),
    ],
}

DETAIL_TPL = (
    '【{name}】{subtitle}。\n'
    '▸ 品牌官方正品，支持七天无理由退换；\n'
    '▸ 全国联保，顺丰包邮，48小时内发货；\n'
    '▸ 售后无忧：质量问题一年内免费换新。\n'
    '商品参数：\n'
    '  型号：{name}（2026款）\n'
    '  颜色：曜石黑 / 皓月白 / 星空灰\n'
    '  包装清单：主机 ×1、说明书 ×1、保修卡 ×1\n'
)


class Command(BaseCommand):
    help = '初始化电商示例数据（分类/商品/测试账号）'

    def handle(self, *args, **options):
        if Category.objects.exists():
            self.stdout.write(self.style.WARNING('已存在分类数据，跳过初始化'))
            return

        cats = {}
        seed = 0
        for cat_name, products in CATS.items():
            cat = Category.objects.create(name=cat_name, sort=len(cats))
            cats[cat_name] = cat
            for i, (name, subtitle, price, original, stock, hot, new) in enumerate(products):
                seed += 1
                cover = cover_url(seed)
                Product.objects.create(
                    category=cat, name=name, subtitle=subtitle,
                    cover=cover, gallery=[cover, cover_url(seed + 100)],
                    price=price, original_price=original, stock=stock,
                    sales=seed * 37 % 900 + 20,
                    detail=DETAIL_TPL.format(name=name, subtitle=subtitle),
                    is_hot=hot, is_new=new,
                )

        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', password='admin123456', nickname='管理员')
        if not User.objects.filter(username='demo').exists():
            User.objects.create_user('demo', password='demo123456', nickname='演示用户', phone='13800000000')

        self.stdout.write(self.style.SUCCESS(
            f'初始化完成：分类 {Category.objects.count()} 个，商品 {Product.objects.count()} 件，'
            '账号 admin/admin123456、demo/demo123456'))
