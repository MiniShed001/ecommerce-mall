from django.apps import AppConfig


class ProductsConfig(AppConfig):
    name = 'apps.products'
    verbose_name = '商品'

    def ready(self):
        from . import signals  # noqa: F401
