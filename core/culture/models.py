from django.db import models
from PIL import Image


class PreBase(models.Model):
    """Родительская модель для маршрутов и экспонатов"""
    name = models.CharField(
        max_length=150,
        verbose_name='Название',
        default='Без названия',
    )
    description = models.TextField(
        verbose_name='Описание',
        default='Без описания',
    )
    image = models.ImageField(
        upload_to='pictures',
        verbose_name='Фото',
        )
    address = models.TextField(verbose_name='Точный адрес')

    def save(self, *args, **kwargs):
        """Изменяется раширение изображения?"""
        super(PreBase, self).save(*args, **kwargs)

        if self.image:
            fixed_width = 1080
            filepath = self.image.path
            img = Image.open(filepath)
            width_percent = (fixed_width / float(img.size[0]))
            height_size = int((float(img.size[1]) * float(width_percent)))
            new_image = img.resize((fixed_width, height_size))
            new_image.save(filepath)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Route(PreBase):
    """Модель для описания маршрутов"""
    route_map = models.ImageField(
        upload_to='pictures',
        verbose_name='Карта маршрута',
        )
    text_route_start = models.TextField(
        verbose_name='Текст к месту начала маршрута',
        blank=True,
    )
    exhibite = models.ManyToManyField(
        'Exhibit',
        through='RouteExhibit',
        related_name='routes',
    )

    class Meta:
        ordering = ['id']
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return f'Маршрут {self.pk}'


class Exhibit(PreBase):
    """Модель для описания объектов"""
    author = models.CharField(
        max_length=100,
        verbose_name='Автор',
        default='Не указан',
    )
    how_to_pass = models.TextField(
        verbose_name='Путь до объекта',
        blank=True,
        )
    message_before_description = models.TextField(
        verbose_name='Подводка',
        blank=True,
        )
    reflection = models.TextField(
        verbose_name='Рефлексии',
        blank=True,
        )
    reflection_positive = models.TextField(
        verbose_name='Сообщение после положительного ответа пользователя',
        blank=True,
        )
    reflection_negative = models.TextField(
        verbose_name='Сообщение после отрицательного ответа пользователя',
        blank=True,
        )
    transfer_message = models.TextField(
        verbose_name='Сообщение для перехода к следующему объекту',
        blank=True,
        )

    class Meta:
        ordering = ['id']
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'

    def __str__(self):
        return f'Объект {self.pk}: {self.name}'


class RouteExhibit (models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        verbose_name='Маршрут',
    )
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        verbose_name='Объекты',
    )

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'
        constraints = [
            models.UniqueConstraint(
                fields=['route', 'exhibit'],
                name='unique_exhibites_route'
            )
        ]

    def __str__(self):
        return f'Объект {self.exhibit.pk}'


class Review(models.Model):
    """Модель для отзывов пользователя"""
    username = models.CharField(
        max_length=100,
        verbose_name='Имя',
        default='Аноним',
    )
    userage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Возраст'
        )
    userhobby = models.CharField(
        max_length=150,
        verbose_name='Хобби',
        default='Не указано',
    )
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Объект',
    )
    answer_to_message_before_description = models.TextField(
        verbose_name='Ответ на подводку',
        default='Вопроса не было.',
        blank=True,
    )
    answer_to_reflection = models.TextField(
        verbose_name='Ответ на рефлексию',
        default='Ответа не было.',
        blank=True,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.pk}'


class FeedBack(models.Model):
    """Модель для опросов пользователя"""
    email = models.EmailField(max_length=254, unique=True)
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        verbose_name='Маршрут',
    )
    text = models.TextField(verbose_name='Отзыв на маршрут')

    class Meta:
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'

    def __str__(self):
        return f'Опрос {self.pk}'
