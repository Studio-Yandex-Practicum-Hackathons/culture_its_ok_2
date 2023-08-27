# Бот АНО "Культура”

![culture_its_ok_2 workflow](https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_2/actions/workflows/culture_its_ok_2.yml/badge.svg)

## Описание
Бот проводит экскурсию-медитацию по местам г. Ростова с работами уличных художников.

Наш бот в телеграме: https://t.me/culture_2_bot

## Запуск проекта на локальной машине

* Установите docker и docker-compose
* Для установки на ubuntu выполните следующие команды:
```
sudo apt install docker.io
sudo apt install docker-compose
```
Про установку на других операционных системах вы можете прочитать в [документации](https://docs.docker.com/engine/install/) и [про установку docker-compose](https://docs.docker.com/compose/install/).

* Склонируйте репозиторий на локальную машину:
```
git clone https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_2.git
```
* В корне проекта создайте .env файл по аналогии с файлом .env.example.
* Перейдите в папку infra и соберите контейнеры:
```
docker-compose up -d
```
* Примените миграции:
```
docker-compose exec web python manage.py migrate
```
* Создайте суперпользователя Django:
```
docker-compose exec web python manage.py createsuperuser
```
* Соберите статику:
```
docker-compose exec web python manage.py collectstatic --noinput
```

* Для заполнения или обновления базы данных по маршрутам и экспонатам, а также для выгрузки отчётов в pdf перейдите по адресу https://localhost/admin
* Перейдите в телеграм и следуйте инструкциям бота.

## Запуск проекта на удаленном сервере
* Склонируйте репозиторий на локальную машину:
```
git clone https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_2.git
```
* В файле settings.py впишите свой IP в следующей строчке: CSRF_TRUSTED_ORIGINS = ['http://your_ip_adress']
* Отредактируйте файл infra/nginx/default.conf и в строке server_name впишите свой IP
* В корне проекта создайте .env файл по аналогии с файлом .env.example.

* Установите docker на сервер:
```
sudo apt install docker.io
```
* Установите docker-compose на сервер:
```
sudo apt install docker-compose
```

* Скопируйте папку infra и файл .env на сервер:
```
scp -r /infra <username>@<host>:/home/<username>/
scp .env <username>@<host>:/home/<username>/
```
* На сервере соберите контейнеры:
```
sudo docker-compose up -d --build
```
* После сборки контейнеров на сервере выполните команды (только после первого деплоя):
    - Примените миграции:
    ```
    sudo docker-compose exec web python manage.py migrate
    ```
    - Создайте суперпользователя Django:
    ```
    sudo docker-compose exec web python manage.py createsuperuser
    ```
    - Соберите статику:
    ```
    sudo docker-compose exec web python manage.py collectstatic --noinput
    ```

* Для заполнения или обновления базы данных по маршрутам и экспонатам, а также для выгрузки отчётов в pdf перейдите по адресу https://your_ip_adress/admin
* Бот готов к работе.
* Перейдите в телеграм и следуйте инструкциям бота.
* Приятной экскурсии!

## Используемые технологии

- [![Python](https://img.shields.io/badge/-Python_3.11-464646?style=flat-square&logo=Python)](https://www.python.org/)
- [![Django](https://img.shields.io/badge/-Django_4.1-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
- [![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
- [![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
- [![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
- [![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
- [![Aiogram](https://img.shields.io/badge/Aiogram-3.0.0rc1-green?logo=Aiogram&logoColor=green)](https://aiogram.dev/)
- [![reportlab](https://img.shields.io/badge/reportlab-4.0.4-green?logo=reportlab&logoColor=green)](https://pypi.org/project/reportlab/)
- [![SpeechRecognition](https://img.shields.io/badge/SpeechRecognition-3.10-green?logo=django_ckeditor&logoColor=green)](https://pypi.org/project/SpeechRecognition/)
- [![django_ckeditor](https://img.shields.io/badge/django_ckeditor-6.7.0-green?logo=django_ckeditor&logoColor=green)](https://pypi.org/project/django-ckeditor/)
- [![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
- [![Google](https://img.shields.io/badge/google-3.0.0-green?logo=google&logoColor=green)](https://pypi.org/project/google/)
- [![google-api-python-client](https://img.shields.io/badge/google_api_python_client-2.97.0-green?logo=google_api_python_client&logoColor=green)](https://pypi.org/project/google-api-python-client/)
- [![bs](https://img.shields.io/badge/bs-4%200.0.1-green?logo=bs&logoColor=green)](https://pypi.org/project/bs4/)
- - django-admin-rangefilter

## Авторы:

**Изимов Арсений**  - студент Яндекс.Практикума Когорта 16+
https://github.com/Arseny13

**Дмитрий Абрамов**  - студент Яндекс.Практикума Когорта 16+
https://github.com/D-Abramoc/

**Вадим Конюшков**  - студент Яндекс.Практикума Когорта 16+
https://github.com/Vadikray

**Алексей Боборыкин**  - студент Яндекс.Практикума Когорта 16+
https://github.com/alexey-boborykin

**Роман Пекарев**  - студент Яндекс.Практикума Когорта 16+
https://github.com/ropek745

**Баранов Виктор**  - студент Яндекс.Практикума Когорта 16+
https://github.com/vityn101979