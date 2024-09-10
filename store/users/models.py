import datetime
import uuid

import django.utils.timezone as timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse_lazy
from django.core.mail import EmailMessage


class User(AbstractUser):
    SEX = [
        ('М', 'Мужчина'),
        ('Ж', 'Женщина'),
        ('Н', 'Скрыто')
    ]

    image = models.ImageField(upload_to='user_images', null=True, blank=True, verbose_name='Изображение пользователя')
    sex = models.CharField(max_length=1, choices=SEX, default='Н', verbose_name='Пол')
    age = models.DateField(verbose_name='Возраст', default=timezone.now)
    is_verified = models.BooleanField(default=False, verbose_name='Подтверждение верификации')

    def __str__(self):
        age = datetime.date.today().year - self.age.year
        return (f'{self.pk}. {self.last_name.title()} {self.first_name.title()} | '
                f'возраст: {age} | '
                f'пол: {self.get_sex_display()}')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class EmailVerification(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False,
                            unique=True, verbose_name='Код подтверждения')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    expiration = models.DateTimeField(verbose_name='Время блокировки')

    def __str__(self):
        return f'{self.created_at} | {self.user} | {self.code}'

    def send_verification_code(self):
        # Формируем ссылку для отправки пользователю для подтверждения
        link = reverse_lazy('users:verify', kwargs={'username': self.user.username, 'code': self.code})
        subject = f"Верификация аккаунта на сайте - {settings.DOMAIN_NAME}"
        message = f"Вы были зарегистрированы на нашем сайте. Просим потдвердить этот аккаунт - " \
        f"{self.user.username} | {self.user.last_name} | {self.user.first_name}.\n" \
        f"Перейдите по этой ссылке для верификации - {settings.DOMAIN_NAME + link}\n" \
        f"Время действия ссылки 1 час!"
        msg = EmailMessage(subject, message, to=[self.user.email])
        msg.send()


    def is_expired(self):
        return timezone.now() > self.expiration

    class Meta:
        verbose_name = 'Верификация'
        verbose_name_plural = 'Верификации'
        ordering = ['created_at']
