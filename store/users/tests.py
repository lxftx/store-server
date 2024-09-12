import datetime
import statistics
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy

from users.forms import UserRegistrationForm
from users.models import EmailVerification, User


class UserRegistrationViewTest(TestCase):

    def setUp(self):
        self.data = {'first_name': 'Test',
                     'last_name': 'Test',
                     'sex': 'Н',
                     'age': datetime.date.today(),
                     'username': 'testBot',
                     'email': 'testBot@gmail.com',
                     'password1': 'Zaserd12sqwe',
                     'password2': 'Zaserd12sqwe'}
        self.path = reverse_lazy('users:register')

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'Store - Регистрация')
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post(self):
        username = self.data['username']
        self.assertFalse(User.objects.filter(username=username).exists())

        response = self.client.post(self.path, data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        # assertRedirects не работает, так как есть django-allauth
        # self.assertRedirects(response, reverse_lazy('users:index'))
        # assertTrue - принимает один аргумент и проверяет вернулось ли значение True или False
        self.assertTrue(User.objects.filter(username=username).exists())

        # Check creating of email verification
        email_verification = EmailVerification.objects.get(user=User.objects.get(username=username))
        self.assertTrue(email_verification)
        self.assertEqual(email_verification.expiration.date(), datetime.date.today() + datetime.timedelta(hours=1))

    def test_user_registration_post_error(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        # assertContains - Пробегается по response.context и ищет переданную запись
        self.assertContains(response, "Пользователь с таким именем уже существует.", html=True)
