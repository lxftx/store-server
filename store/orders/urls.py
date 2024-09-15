from django.urls import path
from orders.views import OrderListView, OrderDetailView, OrderCreateView, SuccessTemplateView, CanceledTemplateView

app_name = 'orders'

urlpatterns = [
    path('order-create/', OrderCreateView.as_view(), name='order-create'),
    path('order-success/', SuccessTemplateView.as_view(), name='order-success'),
    path('order-canceled/', CanceledTemplateView.as_view(), name='order-canceled'),
    path('', OrderListView.as_view(), name='order-list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
