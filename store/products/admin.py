from django.contrib import admin

from products.models import Basket, Product, ProductCategory

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(Basket)


@admin.register(Product)  # Декоратор, который говорит с какой моделью будем работать
class ProductAdmin(admin.ModelAdmin):
    # list_display - метод, который выводит переданные ей поля в кортеже в админ панеле
    list_display = ('name', 'price', 'quantity', 'category')
    # fields = - метод, который выводит переданные поля в записи ввиде листа(кортеж) в админ панеле
    # измененние расположения полей просходит при помощи оборачивания кортежем двух полей и тд.тп.
    fields = ['name', 'description', 'price', ('quantity', 'image'), 'stripe_produc_price_id', 'category']
    # readonly_fields - метод, который помечает поле только для чтения
    readonly_fields = ['price', 'quantity', 'stripe_produc_price_id']
    # search_fields - метод, по который добавляет в админ панеле поле для поиска по переданному поле
    search_fields = ['name']
    # ordering - метод, который сортирует записи в админ панеле по переданному полю
    ordering = ['-name']


# BasketAdmin - будет частью другой, админ панели - User
class BasketAdmin(admin.TabularInline):
    # Указание модели
    model = Basket
    # Какие поля выводит в записи
    fields = ['product', 'quantity', 'create_time_stamp']
    readonly_fields = ['create_time_stamp']
    extra = 0  # Дополнительные поля для добавлении записей для метода inlines, по умолчанию 3
