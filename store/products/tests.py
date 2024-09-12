from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from products.models import Product, ProductCategory
from users.models import User


class IndexViewTests(TestCase):

    def test_view(self):
        path = reverse_lazy('index')  # http://127.0.0.1:8000
        response = self.client.get(path)

        for k, v in response.__dict__.items():
            print(k, v)

        # метод assertEqual - сверяет два объекта на идентичность, если они будут не равны, то выйдет ошибка
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store')
        # метод assertTemplateUsed - сверяет два шаблона на идентичность, если не равны - ошибка.
        self.assertTemplateUsed(response, 'products/index.html')

        # Когда мы делаем тесты, то используется пустая тестовая бд.
        # При работе теста, создается тестовая бд и по окончанию теста она удаляется.
        print(f"User - {User.objects.all()}")
        print(f"Product - {Product.objects.all()}")


class ProductsListViewTests(TestCase):
    # Заполнение тестовой бд с помощью fixtures
    fixtures = ['categories.json', 'products.json']

    # В этой функции setUp - мы можем объявлять нужные нам переменные, для тестов
    def setUp(self):
        self.products = Product.objects.all()

    def test_view(self):
        path = reverse_lazy('products:index')
        response = self.client.get(path)
        # print(response.__dict__)

        self._common_tests(response)
        self.assertListEqual(list(response.context_data['products']), list(self.products[:3]))

    def test_list_categories(self):
        category = ProductCategory.objects.first()
        path = reverse_lazy('products:category', kwargs={'category_id': category.id})
        response = self.client.get(path)

        self._common_tests(response)
        self.assertListEqual(list(response.context_data['products']),
                             list(self.products.filter(category_id=category.id)[:3])
                             )

    # Методы, которые используются только внутри класса, обозначаются вначале _
    # Вынесли некоторый повторяющиеся действия, используя DRY
    def _common_tests(self, response):
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Каталог')
        self.assertTemplateUsed(response, 'products/products.html')
