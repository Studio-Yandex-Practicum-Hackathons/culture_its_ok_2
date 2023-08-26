# Бот АНО -Культура”

## Авторы:

**Изимов Арсений**  - студент Яндекс.Практикума Когорта 16+
https://github.com/Arseny13

**Баранов Виктор**  - студент Яндекс.Практикума Когорта 16+
https://github.com/vityn101979

**Дмитрий Абрамов**  - студент Яндекс.Практикума Когорта 16+
https://github.com/D-Abramoc/

**Вадим Конюшков**  - студент Яндекс.Практикума Когорта 16+
https://github.com/Vadikray

**Алексей Боборыкин**  - студент Яндекс.Практикума Когорта 16+
https://github.com/alexey-boborykin

**Роман Пекарев**  - студент Яндекс.Практикума Когорта 16+
https://github.com/ropek745

## Описание
Данный бот проводит экскурсию-медитацию по местам г.Ростова с работами уличных художников.

## Подготовка к использованию бота
## Склонируйте репозиторий на локальную машину:
```
git clone https://github.com/Studio-Yandex-Practicum-Hackathons/culture_its_ok_2.git
```
* Локально отредактируйте файл infra/nginx.conf и в строке server_name впишите свой IP
* В корне проекта создайте .env файл:
    ```
    TELEGRAM_TOKEN="your_telegram_token"
    SECRET_KEY="secret_key_django"
    ADMIN_ID="id телеграма администратора бота"
    DB_ENGINE= "django.db.backends.postgresql"
    DB_NAME="имя базы данных postgres"
    POSTGRES_USER="пользователь бд"
    POSTGRES_PASSWORD="пароль"
    DB_HOST="db"
    DB_PORT="5432"
    ```

## Запуск проекта на удаленном сервере

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
* На сервере соберите docker-compose:
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

* Для заполнения или обновления базы данных по маршрутам и экспонатам перейдите по адресу https://your_ip_adress/admin и внесите необходимые изменения
* Бот готов к работе. Перейдите в телеграм и следуйте инструкциям бота. Приятной экскурсии.

## Используемые технологии

- Python 3.11
- Django 4.1
- Aiogram 3.0.0rc1
- reportlab 4.0.4
- SpeechRecognition 3.10
- django_ckeditor 6.7.0


Cписок будет пополняться.
