from django.urls import include, path

urlpatterns = [
    path('auth/', include('apps.users.urls')),
    path('', include('apps.products.urls')),
    path('', include('apps.carts.urls')),
    path('', include('apps.orders.urls')),
]
