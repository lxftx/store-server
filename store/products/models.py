from django.db import models

from users.models import User


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
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE, verbose_name="Категория товара",
                                 default='Категория не выбрана', blank=True, null=True)

    def __str__(self):
        return f'Вещь: {self.name} | Цена: {self.price}₽ | Категория: {self.category}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class BasketQuerySet(models.QuerySet):
    def total_price(self):
        return sum([price.sum() for price in self.filter()])

    def total_quantity(self):
        return sum([quantity.quantity for quantity in self.filter()])


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
