from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from users.tasks import send_email_verification

from users.models import User


class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        print(kwargs.get('instance'))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))

    class Meta:
        model = User
        fields = ('login', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите имя пользователя'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите фамилию пользователя'
    }))
    sex = forms.ChoiceField(choices=User.SEX, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    age = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите дату рождения пользователя',
        'type': 'date'
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите логин пользователя'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите почту пользователя',
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите пароль'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Повторите введённый пароль'
    }))

    # Этот метод будет отрабатываться, когда форма выполниться. Метод отправляет на указанную почту код верификации
    def save(self, commit=True):
        # Метод save, возвращает объект User
        user = super(UserRegistrationForm, self).save(commit=True)
        print(user)
        send_email_verification.delay(user.id)
        return user

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'sex', 'age', 'username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #   super(UserProfileForm, self).__init__(*args, **kwargs)
    #   print(kwargs.get('instance'))

    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    sex = forms.ChoiceField(choices=User.SEX, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    age = forms.DateField(widget=forms.DateInput(
        format='%Y-%m-%d',
        attrs={
            'class': 'form-control',
            'type': 'date',

        }))
    image = forms.ImageField(widget=forms.FileInput(attrs={
        'type': 'file',
        'class': 'custom-file-input'
    }), required=False)
    username = forms.CharField(disabled=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
    }))
    email = forms.EmailField(disabled=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'sex', 'age', 'image', 'username', 'email')
