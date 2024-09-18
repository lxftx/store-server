from django.urls import path
from django.views.decorators.cache import cache_page

from products.views import ProductListView, basket_add, basket_remove

app_name = 'products'   # переменная которая говорит какое это приложение, если мы используем include на проекте

urlpatterns = [
    path('', ProductListView.as_view(), name='index'),   # name - для динамической url ссылки
    # cache_page - кэшируем страницу (грубый режим) на 30 секунд
    path('category/<str:category_id>/', ProductListView.as_view(), name='category'),
    path('page/<int:page>/', ProductListView.as_view(), name='paginator'),
    path('baskets/add/<int:product_id>/', basket_add, name='basket_add'),
    path('baskets/delete/<int:product_id>/', basket_remove, name='basket_remove'),
]
