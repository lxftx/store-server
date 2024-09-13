# docker-compose build
# docker-compose upp
# docker-compose run --rm web-app sh -c "python manage.py makemigtations"


FROM python:3.12.5-alpine3.20

COPY requirements.txt /temp/requirements.txt
COPY store /store
WORKDIR /store
# EXPOSE Получение доступа снаружи, т.е с нашей операционной системы
EXPOSE 8000

# Установка зависимости подключения postgesql к python
RUN apk add postgresql-client build-base postgresql-dev

# Установка зависимости
RUN pip install -r /temp/requirements.txt

# Эта команда создаст пользователя в операционной системе, --disabled-password пароль не нужен, доступ только у нас, server-user название у сервиса
RUN adduser --disabled-password store-user

# Пользователь под которым вызываются все команды
USER store-user