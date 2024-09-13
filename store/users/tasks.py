# Файл для Selery Worker 
import datetime
import uuid

from celery import shared_task

@shared_task
def send_email_verification(user_id):
    from users.models import User, EmailVerification
    user = User.objects.get(id=user_id)
    expiration = datetime.datetime.now() + datetime.timedelta(hours=1)
    record = EmailVerification.objects.create(code=uuid.uuid4(), user=user, expiration=expiration)
    # Вызов метода с модели, отправки кода верификации
    record.send_verification_code()

@shared_task
def print_hello():
    print('Hello, Gay!')