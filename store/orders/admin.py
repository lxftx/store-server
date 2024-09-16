from django.contrib import admin

from orders.models import Orders


@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'status')
    fields = (
        'id',
        'status',
        ('first_name', 'last_name'),
        ('email', 'address'),
        'basket_history',
        'user'
    )
    readonly_fields = ('id', 'first_name', 'last_name', 'email', 'address', 'created', 'user', 'basket_history')
