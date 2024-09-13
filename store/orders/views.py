from django.shortcuts import render
from django.views.generic.edit import CreateView
from orders.forms import OrderForm
from django.urls import reverse_lazy
from orders.models import Orders
from common.views import TitleMixin


class OrderCreateView(TitleMixin, CreateView):
    model = Orders
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    title = 'Store - Оформление заказа'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('users:profile', args={self.request.user.id,})