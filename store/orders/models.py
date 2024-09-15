from django.db import models
from users.models import User
from products.models import Basket


class Orders(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERIED = 3
    STATUSES = (
        (CREATED, 'Создан'),
        (PAID, 'Оплачен'),
        (ON_WAY, 'В пути'),
        (DELIVERIED, 'Доставлен'),
    )

    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    email = models.EmailField(max_length=256, verbose_name='Адрес электронной почты')
    address = models.CharField(max_length=256, verbose_name='Адрес')
    created = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    basket_history = models.JSONField(default=dict, verbose_name='Товары')
    status = models.SmallIntegerField(choices=STATUSES, default=CREATED, verbose_name='Статус')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Заказывал')

    def __str__(self):
        return f"Заказ №{self.id} | Для пользователя - {self.last_name} {self.first_name}."

    def update_for_history(self):
        basket = Basket.objects.filter(user=self.user)
        self.status = self.PAID
        self.basket_history = {
            'items': [item.de_json() for item in basket],
            'total_sum': float(basket.total_price())
        }
        basket.delete()
        self.save()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-id']
