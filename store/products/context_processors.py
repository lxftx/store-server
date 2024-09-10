from products.models import Basket


# Этот контекстный процессор может быть получен из любого шаблона, главное указать в настройках
# Функция baskets выводит корзину для авторизованного пользователя
def baskets(request):
    if request.user.is_authenticated:
        baskets = Basket.objects.filter(user=request.user)
    else:
        baskets = []
    return {'baskets': baskets}
