from django.db import models


class PreBase(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        unique=True,
    )
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(
        upload_to='pictures',
        verbose_name='Фото',
        )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Base(models.Model):
    username = models.CharField(
        max_length=50,
        verbose_name='Имя'
    )
    userage = models.IntegerField(
        blank=True,
        null=True,
        verbose_name='Возраст'
        )
    userhobby = models.CharField(
        max_length=150,
        verbose_name='Хобби',
    )
    text = models.TextField(verbose_name='Отзыв')

    class Meta:
        abstract = True


class Route(PreBase):

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'


    def __str__(self):
        return f'Маршрут {self.pk}'



class Exhibit(PreBase):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name='exhibit',
    )

    class Meta:
        verbose_name = 'Экспонат'
        verbose_name_plural = 'Экспонаты'


    def __str__(self):
        return f'Экспонат {self.pk}'


class Comment(Base):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'Комментарий {self.pk}'


class FeedBack(Base):

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f'Отзыв {self.pk}'
