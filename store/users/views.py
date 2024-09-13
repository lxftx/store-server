from django.conf import settings
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class SignUpView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Store - Авторизация'

    def get_success_url(self):
        return reverse_lazy('index')

# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)  # data - обязательно
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse_lazy('index'))
#     else:
#         form = UserLoginForm()
#     context = {'form': form}
#     return render(request, 'users/login.html', context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:index')
    title = 'Store - Регистрация'
    success_message = 'Удачная регистрация!'


# def register(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             form.clean()
#             messages.success(request, 'Удачная регистрация!')  # Библиотека которая помогает работать с сообщениями в
#             # шаблонах
#             print(messages)
#             return HttpResponseRedirect(reverse_lazy('users:index'))
#     else:
#         form = UserRegistrationForm()
#     context = {'form': form}
#     return render(request, 'users/register.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('index'))



class UserUpdateView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Store - Личный кабинет'

    # Переопределили метод, для передачи id в информации о пользователе
    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))

    # Эта функция ставится не нужной, так как есть контекстный процессор baskets в приложении products
    # def get_context_data(self, **kwargs):
    #     context = super(UserUpdateView, self).get_context_data(**kwargs)
    #     context['baskets'] = Basket.objects.filter(user=self.object)
    #     return context

# Декоратор, который перенаправляет пользователя на указанную ссылку, если он не авторизован
# @login_required(login_url=settings.LOGIN_URL)
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse_lazy('users:profile'))
#     else:
#         form = UserProfileForm(instance=request.user)
#     model = Basket.objects.filter(user=request.user)
#     # Расчеты выполняются в products.models
#     # total_price = sum([price.sum() for price in model])
#     # total_quantity = sum([quantity.quantity for quantity in model])
#     context = {'title': 'Store - профиль',
#                'form': form,
#                'user': request.user,
#                'baskets': model
#                }
#     return render(request, 'users/profile.html', context)


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Store - Подтверждение электронной почты'

    # Функция get, отвечает за вызов передачу GET запроса
    def get(self, request, *args, **kwargs):
        code = kwargs.get('code', None)
        user = User.objects.get(username=kwargs.get('username', None))
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        # exists() - Если наш список не пустой
        if email_verifications.exists() and not email_verifications.first().is_expired() and not user.is_verified:
            user.is_verified = True
            user.save()
            # Возвращаем метод, чтобы метод get выполнился
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse_lazy('index'))
