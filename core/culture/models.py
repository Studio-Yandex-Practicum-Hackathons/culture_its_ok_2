from ckeditor.fields import RichTextField
from django.db import models
from django.utils.safestring import mark_safe

from .utils import prepare_image



class PreBase(models.Model):
    """Родительская модель для маршрутов и экспонатов"""

    name = models.CharField(
        max_length=150,
        verbose_name="Название",
        default="Без названия",
    )
    description = RichTextField(
        verbose_name="Описание",
        default="Без описания",
    )
    address = RichTextField(verbose_name="Точный адрес")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Route(PreBase):
    """Модель для описания маршрутов.
    Эта модель связана с моделью Exhibit посредством модели RouteExhibit.
    """

    image = models.ImageField(
        upload_to="routes",
        verbose_name="Фото",
    )
    route_map = models.ImageField(
        upload_to="routes_map",
        verbose_name="Карта маршрута",
    )
    text_route_start = RichTextField(
        verbose_name="Текст к месту начала маршрута",
        blank=True,
    )
    exhibite = models.ManyToManyField(
        "Exhibit",
        through="RouteExhibit",
        related_name="routes",
    )

    def save(self, *args, **kwargs):
        """Обработка изображения перед сохранением в базу данных"""

        super(Route, self).save(*args, **kwargs)

        if self.image:
            filepath = self.image.path
            prepare_image(self.image, filepath)

        if self.route_map:
            filepath = self.route_map.path
            prepare_image(self.route_map, filepath)

    class Meta:
        ordering = ["id"]
        verbose_name = "Маршрут"
        verbose_name_plural = "Маршруты"

    def __str__(self):
        return f"Маршрут {self.pk}"


class Exhibit(PreBase):
    """Модель для описания объектов.
    Эта модель связана с моделью Photo посредством модели ExhibitPhoto.
    """

    author = models.CharField(
        max_length=100,
        verbose_name="Автор",
        default="Не указан",
    )
    how_to_pass = RichTextField(
        verbose_name="Путь до объекта",
        blank=True,
    )
    message_before_description = RichTextField(
        verbose_name="Подводка",
        blank=True,
    )
    reflection = RichTextField(
        verbose_name="Рефлексии",
        blank=True,
    )
    reflection_positive = RichTextField(
        verbose_name="Сообщение после положительного ответа пользователя",
        blank=True,
    )
    reflection_negative = RichTextField(
        verbose_name="Сообщение после отрицательного ответа пользователя",
        blank=True,
    )
    transfer_message = RichTextField(
        verbose_name="Сообщение для перехода к следующему объекту",
        blank=True,
    )
    image = models.ManyToManyField(
        "Photo",
        through="ExhibitPhoto",
        related_name="exhibits",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"

    def __str__(self):
        return f"Объект {self.pk}: {self.name}"


class RouteExhibit(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        verbose_name="Маршрут",
    )
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        verbose_name="Объекты",
    )

    class Meta:
        verbose_name = "Объект"
        verbose_name_plural = "Объекты"
        constraints = [
            models.UniqueConstraint(
                fields=["route", "exhibit"], name="unique_exhibites_route"
            )
        ]

    def __str__(self):
        return f"Объект {self.exhibit.pk}"


class Photo(models.Model):
    """Модель для фотографий объектов"""

    image = models.ImageField(
        upload_to="exhibit",
        verbose_name="Фото",
    )

    def save(self, *args, **kwargs):
        """Изменяется разрешение изображения"""

        super(Photo, self).save(*args, **kwargs)

        if self.image:
            filepath = self.image.path
            prepare_image(self.image, filepath)

    def img_preview(self):
        return mark_safe(
            f'<img src="{self.image.url}" style="max-height: 300px;">')

    def __str__(self):
        return f"Фото {self.pk}"


class ExhibitPhoto(models.Model):
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        verbose_name="Объекты",
    )
    photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE,
        verbose_name="Фото",
    )

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"
        constraints = [
            models.UniqueConstraint(
                fields=["exhibit", "photo"], name="unique_photos_exhibit"
            )
        ]

    def __str__(self):
        return f"Объект {self.photo.pk}"


class Review(models.Model):
    """Модель для отзывов пользователя.
    Модель связана с моделью Exhibit
    """

    username = models.CharField(
        max_length=100,
        verbose_name="Имя",
        default="Аноним",
    )
    userage = models.IntegerField(
        blank=True, null=True, verbose_name="Возраст"
    )
    userhobby = models.CharField(
        max_length=150,
        verbose_name="Хобби",
        default="Не указано",
    )
    exhibit = models.ForeignKey(
        Exhibit,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Объект",
    )
    answer_to_message_before_description = models.TextField(
        verbose_name="Ответ на подводку",
        default="Вопроса не было.",
        blank=True,
        null=True,
    )
    answer_to_reflection = models.TextField(
        verbose_name="Ответ на рефлексию",
        default="Ответа не было.",
        blank=True,
        null=True,
    )
    text = models.TextField(verbose_name="Текст отзыва")
    created_at = models.DateField(
        verbose_name="Дата создания",
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f"Отзыв {self.pk}"


class FeedBack(models.Model):
    """Модель для опросов пользователя.
    Модель связана с моделью Route
    """

    email = models.EmailField(max_length=254, unique=True)
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        verbose_name="Маршрут",
    )
    text = models.TextField(verbose_name="Отзыв на маршрут")

    class Meta:
        verbose_name = "Опрос"
        verbose_name_plural = "Опросы"

    def __str__(self):
        return f"Опрос {self.pk}"
