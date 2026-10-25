from django.urls import path

from . import views

urlpatterns = [
    path('orders/', views.OrderCreateView.as_view()),
    path('orders/list/', views.OrderListView.as_view()),
    path('orders/<int:pk>/', views.OrderDetailView.as_view()),
    path('orders/<int:pk>/pay/', views.OrderPayView.as_view()),
    path('orders/<int:pk>/cancel/', views.OrderCancelView.as_view()),
]
