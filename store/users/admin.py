from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_verified')
    fields = ['username', 'first_name', 'last_name', 'email', 'age', 'sex', 'is_verified']
    readonly_fields = ['is_verified']
    inlines = [BasketAdmin, ]  # Как бы говорим, чтобы записи имеющие связь с моделью Basket выводились в User


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'user')
    fields = ('user', 'code', 'created_at', 'expiration')
    readonly_fields = ('user', 'code', 'expiration', 'created_at',)
