import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exhibit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Без названия', max_length=150, verbose_name='Название')),
                ('description', models.TextField(default='Без описания', verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pictures', verbose_name='Фото')),
                ('address', models.TextField(verbose_name='Точный адрес')),
                ('author', models.CharField(max_length=100, verbose_name='Автор')),
                ('how_to_pass', models.TextField(blank=True, verbose_name='Путь до объекта')),
                ('message_before_description', models.TextField(blank=True, verbose_name='Сообщение перед описанием объекта')),
                ('message_before_review', models.TextField(blank=True, verbose_name='Сообщение перед комментарием пользователя')),
                ('message_after_review', models.TextField(blank=True, verbose_name='Сообщение после комментария пользователя')),
                ('transfer_message', models.TextField(blank=True, verbose_name='Сообщение для перехода к следующему объекту')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='FeedBack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='Аноним', max_length=100, verbose_name='Имя')),
                ('userage', models.IntegerField(blank=True, null=True, verbose_name='Возраст')),
                ('userhobby', models.CharField(default='Не указано', max_length=150, verbose_name='Хобби')),
                ('text', models.TextField(verbose_name='Отзыв')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Без названия', max_length=150, verbose_name='Название')),
                ('description', models.TextField(default='Без описания', verbose_name='Описание')),
                ('image', models.ImageField(blank=True, null=True, upload_to='pictures', verbose_name='Фото')),
                ('address', models.TextField(verbose_name='Точный адрес')),
            ],
            options={
                'verbose_name': 'Маршрут',
                'verbose_name_plural': 'Маршруты',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='RouteExhibit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exhibit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture.exhibit', verbose_name='Объекты')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='culture.route', verbose_name='Маршрут')),
            ],
            options={
                'verbose_name': 'Объект',
                'verbose_name_plural': 'Объекты',
            },
        ),
        migrations.AddField(
            model_name='route',
            name='exhibite',
            field=models.ManyToManyField(related_name='routes', through='culture.RouteExhibit', to='culture.exhibit'),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='Аноним', max_length=100, verbose_name='Имя')),
                ('userage', models.IntegerField(blank=True, null=True, verbose_name='Возраст')),
                ('userhobby', models.CharField(default='Не указано', max_length=150, verbose_name='Хобби')),
                ('text', models.TextField(verbose_name='Отзыв')),
                ('exhibit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='culture.exhibit', verbose_name='Объект')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.AddConstraint(
            model_name='routeexhibit',
            constraint=models.UniqueConstraint(fields=('route', 'exhibit'), name='unique_exhibites_route'),
        ),
    ]
