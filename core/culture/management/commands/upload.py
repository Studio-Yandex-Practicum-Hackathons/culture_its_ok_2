from typing import Any, Optional, Union

from django.core.management import BaseCommand
from docx import Document
from docx.text.paragraph import Paragraph

from core.settings import BASE_DIR
from culture.models import Route

FIELDS = {
    'маршрут': ('name', '.'),
    'описание маршрута': ('description', ':'),
    'начало маршрута': ('address', ':')
}


class Command(BaseCommand):
    help = 'Загрузка данных в БД.'

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        doc: Document = Document(BASE_DIR + r'/data/Route_1/doc_for_test.docx')
        model_fields = [field.name for field in Route._meta.get_fields()]
        paragraphs = self._find_first_paragraph_with_data(doc.paragraphs)
        if not paragraphs:
            self.stdout.write('В документе нет необходимых данных или '
                              'документ составлен не правильно.')
        else:
            dt, paragraphs = self._create_route(paragraphs)
            Route.objects.create(**dt)

    def _create_route(self, paragraphs: list[Paragraph], stop: str = 'объект', data: dict = {}) -> dict[str,str]:
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
            return self._create_route(paragraphs[1:], stop, data)

    def _find_first_paragraph_with_data(
            self, paragraphs: list[Paragraph]
    ) -> Optional[list[Paragraph]]:
        for paragraph in paragraphs:
            text: Optional[str] = paragraph.text
            if text.lower().startswith(('маршрут', 'объект')):
                return paragraphs
            return self._find_first_paragraph_with_data(paragraphs[1:])
