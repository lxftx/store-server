from http import HTTPStatus

import stripe
from django.conf import settings
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from common.views import TitleMixin
from orders.forms import OrderForm
from orders.models import Orders
from products.models import Basket

stripe.api_key = settings.STRIPE_SECRET_KEY


class SuccessTemplateView(TitleMixin, TemplateView):
    template_name = 'orders/success.html'
    title = 'Store - Спасибо за заказ!'


class CanceledTemplateView(TemplateView):
    template_name = 'orders/canceled.html'


class OrderListView(TitleMixin, ListView):
    model = Orders
    template_name = 'orders/orders.html'
    title = 'Store - Заказы'
    context_object_name = 'orders'

    # Фильтрация
    # ordering = ('id')

    def get_queryset(self):
        queryset = super(OrderListView, self).get_queryset()
        return queryset.filter(user=self.request.user)


class OrderDetailView(DetailView):
    template_name = 'orders/order.html'
    model = Orders
    context_object_name = 'orders'

    def get_queryset(self):
        queryset = super(OrderDetailView, self).get_queryset()
        return queryset.filter(id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Store - Заказ №{self.object.id}'
        return context


class OrderCreateView(TitleMixin, CreateView):
    model = Orders
    template_name = 'orders/order-create.html'
    form_class = OrderForm
    title = 'Store - Оформление заказа'

    def post(self, request, *args, **kwargs):
        super(OrderCreateView, self).post(request, *args, **kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        checkout_session = stripe.checkout.Session.create(
            line_items=baskets.create_stripe_products(),
            # self.objects - глобальная переменная в данном классе CreateView
            # т.к идет работа (создание объекта) с этим объектом.
            metadata={'order_id': self.object.id},
            mode='payment',
            success_url=settings.DOMAIN_NAME + reverse_lazy('orders:order-success'),
            cancel_url=settings.DOMAIN_NAME + reverse_lazy('orders:order-canceled'),
        )
        return HttpResponseRedirect(checkout_session.url, status=HTTPStatus.SEE_OTHER)

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(OrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('users:profile', args={self.request.user.id, })


@csrf_exempt
def stripe_webhook_view(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET_KEY
        )
    except ValueError:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        # Invalid signature
        return HttpResponse(status=400)
    if (
            event['type'] == 'checkout.session.completed'
            or event['type'] == 'checkout.session.async_payment_succeeded'
    ):
        fulfill_checkout(event['data']['object'])

    return HttpResponse(status=200)


def fulfill_checkout(session_id):
    order_id = int(session_id.metadata.order_id)
    order = Orders.objects.get(id=order_id)
    order.update_for_history()
    print("Fulfilling Checkout Session", order_id)
