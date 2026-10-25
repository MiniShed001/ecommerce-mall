from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'sort')
    list_editable = ('sort',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'stock', 'sales', 'is_hot', 'is_new', 'status')
    list_filter = ('category', 'is_hot', 'is_new', 'status')
    search_fields = ('name',)
    list_editable = ('price', 'stock', 'is_hot', 'is_new', 'status')
