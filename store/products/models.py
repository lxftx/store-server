from typing import Iterable
import stripe

from django.db import models
from django.conf import settings

from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя категории товара", unique=True)
    # blank=True поле становится не обязательным для заполнения
    description = models.TextField(verbose_name='Описание категории', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=120, verbose_name='Имя продукта')
    description = models.TextField(verbose_name='Описание продукта', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продукта')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество продукта на складе')
    image = models.ImageField(upload_to='product_images/', verbose_name="Изображение продукта")
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name="Категория товара")
    stripe_produc_price_id = models.CharField(max_length=256, null=True, blank=True, verbose_name='ID STRIPE')

    def __str__(self):
        return f'Вещь: {self.name} | Цена: {self.price}₽ | Категория: {self.category}'

    # До того, как должен отработать метод save, т.е пока не срабатывает super(). Мы добавляем в строку 
    # stripe_produc_price_id - значение, а после этого происходит сохранение объекта в super()
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        if not self.stripe_produc_price_id:
            stripe_product_price = self.create_stripe_product_price()
            self.stripe_produc_price_id = stripe_product_price.get('id')
        return super(Product, self).save(force_insert, force_update, using, update_fields)

    def create_stripe_product_price(self):
        stripe_product = stripe.Product.create(name=self.name)
        stripe_product_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=round(self.price * 100),
            currency='rub'
        )
        return stripe_product_price

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        return sum([price.sum() for price in self.filter()])

    def total_quantity(self):
        return sum([quantity.quantity for quantity in self.filter()])

    def create_stripe_products(self):
        line_items = []
        for item in self:
            line_items.append(
                {
                    'price': item.product.stripe_produc_price_id,
                    'quantity': item.quantity,
                }
            )
        return line_items


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Имя пользователя')
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE, verbose_name='Выбранный продукт')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество выбранных товаров')
    create_time_stamp = models.DateTimeField(auto_now_add=True, verbose_name="Время добавления в корзину")
    # Переопределили менеджер пакетов objects, указав с каким классом ему работать
    # и добавили два метода total_price, total_quantity к существующим last(), first(), all() и тд...
    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return (f'Продукт: {self.product.name} | '
                f'Пользователь: {self.user.first_name + ' ' + self.user.last_name} | '
                f'в количестве: {self.quantity}')

    def sum(self):
        return self.quantity * self.product.price

    # Возвращает json объект с информацией о заказе
    def de_json(self):
        basket_item = {
            'name': self.product.name,
            'quantity': self.quantity,
            'price': float(self.product.price),
            'total_price': float(self.sum())
        }
        return basket_item

    # Расчет происходит в классе BasketQuerySet
    # def total_price(self):
    #     model = Basket.objects.filter(user=self.user)
    #     return sum([price.sum() for price in model])
    #
    # def total_quantity(self):
    #     model = Basket.objects.filter(user=self.user)
    #     return sum([quantity.quantity for quantity in model])

    class Meta:
        verbose_name = 'Корзина товаров'
        verbose_name_plural = "Корзины товаров"
