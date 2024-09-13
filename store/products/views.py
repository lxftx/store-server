from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import \
    Paginator  # Класс Paginator для работы с пагинацией
from django.shortcuts import HttpResponseRedirect, render
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache
from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'

    # Функция эта не нужна, так как есть миксин = TitleMixin, который собирает информацию о заголовках
    # get_context_data - метод, который собирает context
    # def get_context_data(self, **kwargs):
    #   переопределяем метод, т.к класс TemplateView имеет этот метод
    #   context = super(IndexView, self).get_context_data(**kwargs)
    #   return context


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    # переопределение переменной object_list = Product.objects.all()
    context_object_name = 'products'
    # Пагинация на странице с использованием объекта page_obj
    paginate_by = 3
    title = 'Store - Каталог'

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        # Получаем переданный id со страницы "category/<str:category_id>/"
        category_id = self.kwargs.get('category_id')
        if category_id:
            return queryset.filter(category_id=category_id)
        else:
            return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        # Установка кэша
        categories = cache.get('categories')
        # Если мы кэш не находим
        if not categories:
            # То мы его устанавливаем на 30 секунд
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            # Если он все же есть, то отдаем
            context['categories'] = categories
        return context


# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()
#
#     per_page = 3
#     paginator = Paginator(object_list=products, per_page=per_page)
#     products_paginator = paginator.page(page_number)
#
#     context = {
#         'title': 'Store - Каталог', 'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#     return render(request, 'products/products.html', context)


"""
create() - создание записи
all() - взять все данные
filter() - WHERE AT SQL
get() - достать запись по атрибуту
"""


# Декоратор, который перенаправляет пользователя на указанную ссылку, если он не авторизован
@login_required(login_url=settings.LOGIN_URL)
def basket_add(request, product_id):
    product = Product.objects.get(pk=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, product_id):
    basket = Basket.objects.get(pk=product_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
