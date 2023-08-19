from PIL import Image
from django.db import models


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
        blank=True,
        null=True,
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


class Base(models.Model):
    """Родительская модель для комментариев и отзывов"""
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
    text = models.TextField(verbose_name='Отзыв')

    class Meta:
        abstract = True


class Route(PreBase):
    """Модель для описания маршрутов"""
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
        verbose_name='Сообщение перед описанием объекта',
        blank=True,
        )
    message_before_review = models.TextField(
        verbose_name='Сообщение перед комментарием пользователя',
        default='Напишите, что вы думаете об этом?'
        )
    message_after_review = models.TextField(
        verbose_name='Сообщение после комментария пользователя',
        default='Спасибо! Ваше мнение очень важно для нас!'
        )
    transfer_message = models.TextField(
        verbose_name='Сообщение для перехода к следующему объекту',
        default='Отлично, идем дальше!'
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


class Review(Base):
    """Модель для комментариев пользователя"""
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Объект',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.pk}'


class FeedBack(Base):
    """Модель для отзывов пользователя"""

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.pk}'
