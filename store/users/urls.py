from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import (EmailVerificationView, LogOutView, SignUpView,
                         UserRegistrationView, UserUpdateView)

app_name = 'users'

urlpatterns = [
    path('', SignUpView.as_view(), name='index'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogOutView.as_view(), name='logout'),
    # login_required - эта же функция = декоратор, который перенаправляет пользователя на указанную ссылку,
    # если он не авторизован @login_required(login_url=settings.LOGIN_URL)
    path('profile/<int:pk>/', login_required(UserUpdateView.as_view()), name='profile'),
    path('verify/<str:username>/<uuid:code>/', EmailVerificationView.as_view(), name='verify')
]
