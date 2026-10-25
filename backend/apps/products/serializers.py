from rest_framework import serializers

from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon', 'sort']


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'subtitle', 'cover', 'price', 'original_price',
                  'sales', 'is_hot', 'is_new', 'category_name']


class ProductDetailSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'subtitle', 'cover', 'gallery', 'price', 'original_price',
                  'stock', 'sales', 'detail', 'is_hot', 'is_new', 'category_name', 'created_at']
