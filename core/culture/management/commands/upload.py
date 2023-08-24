from typing import Any, Optional

from django.core.files import File
from django.core.management import BaseCommand, CommandError
from django.db.models import Model
from docx import Document
from docx.text.paragraph import Paragraph

from core.settings import BASE_DIR
from culture.models import Exhibit, Route

FIELDS = {
    'маршрут': ('name', '.'),
    'описание маршрута': ('description', ':'),
    'начало маршрута': ('address', ':')
}
ROUTE_FIELDS = [('маршрут', '. ', 'name'),
                ('начало маршрута', ': ', 'address'),
                ('описание маршрута', ': ', 'description'),]
EXHIBIT_FIELDS = [
    ('название работы', ': ', 'name'),
    ('автор', ': ', 'author'),
    ('точный адрес', ': ', 'address'),
    ('как пройти', ': ', 'how_to_pass'),
    ('описательный текст', ': ', 'description'),
    ('подводка', ': ', 'message_before_description'),
    ('рефлексия', ': ', 'reflection'),
    ('если ответил да', ': ', 'reflection_positive'),
    ('если ответил нет', ': ', 'reflection_negative'),
    ('текст перехода', ': ', 'transfer_message')
]


class UploadError(CommandError):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def __str__(self):
        return self.message


class Command(BaseCommand):
    help = 'Загрузка данных в БД.'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        doc: Document = Document(BASE_DIR + r'/data/Route_1/fake_route_1.docx')
        paragraphs = self._find_first_paragraph_with_data(
            doc.paragraphs, start_with='маршрут'
        )
        self._check_paragraphs(paragraphs)
        data, paragraphs = self._create_data(paragraphs, ROUTE_FIELDS, data={})
        model = self._create_model(data, Route)
        model.image.save(
            'img.JPG',
            File(
                open(
                    (f'{BASE_DIR}{r"/data/Route_1/"}'
                     f'{r"1. Максим Има. Руки бы им всем оторвать.jpg"}'), 'rb'
                )
            )
        )
        exhibits: list[Exhibit] = self._exhibits(paragraphs, exhibits=[])
        exhibits_to_route: list[int] = [exhibit.id for exhibit in exhibits]
        model.exhibite.add(*exhibits_to_route)
        self._check_paragraphs(paragraphs)
        # paragraphs = self._find_first_paragraph_with_data(
        #     paragraphs, start_with='объект'
        # )
        # self._check_paragraphs(paragraphs)
        # data, paragraphs = self._create_data(
        #     paragraphs, EXHIBIT_FIELDS, data={}
        # )
        # model = self._create_model(data, Exhibit)
        # model.image.save(
        #     'img.JPG',
        #     File(
        #         open(
        #             (f'{BASE_DIR}{r"/data/Route_1/"}'
        #              f'{r"1. Максим Има. Руки бы им всем оторвать.jpg"}'), 'rb'
        #         )
        #     )
        # )
        print('OOOO!')

    def _exhibits(
            self, paragraphs, exhibits: list[Optional[int]]
    ) -> list[Exhibit]:
        # add exit from recursion
        paragraphs = self._find_first_paragraph_with_data(
            paragraphs, start_with='объект'
        )
        if paragraphs is None:
            return exhibits
        # parse data for exhibit
        data, paragraphs = self._create_data(paragraphs,
                                             EXHIBIT_FIELDS, data={})
        # create exhibit
        model = self._create_model(data, Exhibit)
        # find photo
        # add photo
        model.image.save(
            'img.JPG',
            File(
                open(
                    (f'{BASE_DIR}{r"/data/Route_1/"}'
                     f'{r"1. Максим Има. Руки бы им всем оторвать.jpg"}'), 'rb'
                )
            )
        )
        # add model.id to exhibits
        exhibits.append(model)
        return self._exhibits(paragraphs, exhibits)

    def _create_data(
            self, paragraphs, fields, data={}
    ) -> tuple[dict[str, str], list[Paragraph]]:
        for paragraph in paragraphs:
            text: str = paragraph.text
            if len(fields) == 0:
                return data, paragraphs
            if text == '':
                return self._create_data(paragraphs[1:], fields, data)
            if text.lower().startswith(fields[0][0]):
                _, data[fields[0][2]] = text.split(fields[0][1], 1)
                return self._create_data(paragraphs[1:], fields[1:], data)
            return self._create_data(paragraphs[1:], fields, data)

    def _create_data_route(
            self, paragraphs: list[Paragraph], stop: str = 'объект',
            data: dict = {}
    ) -> dict[str, str]:
        '''
        Формирует словарь для создания модели.
        '''
        data = data
        for paragraph in paragraphs:
            text: Optional[str] = paragraph.text
            if text.lower().startswith(stop):
                return data, paragraphs
            if text.lower().startswith(tuple(FIELDS.keys())):
                if text.lower().startswith('маршрут'):
                    _, name = text.split('.', 1)
                    name.strip()
                    data['name'] = name
                elif text.lower().startswith('описание маршрута'):
                    _, description = text.split(':', 1)
                    description.strip()
                    data['description'] = description
                elif text.lower().startswith('начало маршрута'):
                    _, address = text.split(':', 1)
                    data['address'] = address.strip()
            return self._create_data_route(paragraphs[1:], stop, data)

    def _find_first_paragraph_with_data(
            self, paragraphs: list[Paragraph], start_with: str
    ) -> Optional[list[Paragraph]]:
        for paragraph in paragraphs:
            text: Optional[str] = paragraph.text
            if text.lower().startswith(start_with):
                return paragraphs
            return self._find_first_paragraph_with_data(
                paragraphs[1:], start_with
            )

    def _create_model(self, data: dict[str, str], model: Model) -> Model:
        return model.objects.create(**data)

    def _check_paragraphs(self, paragraphs):
        if paragraphs is None:
            raise UploadError('В документе нет необходимых данных или '
                              'документ составлен не правильно.')
