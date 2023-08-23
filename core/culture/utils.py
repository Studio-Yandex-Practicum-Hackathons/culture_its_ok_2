import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table, TableStyle, colors

TABLE_HEADER = [
    "Имя",
    "Возраст",
    "Хобби",
    "Объект",
    "Ответ на подводку",
    "Ответ на рефлексию",
    "Текст отзыва",
]

styles = getSampleStyleSheet()

pdfmetrics.registerFont(
    TTFont(
        "Helvetica",
        os.path.join(settings.FONTS_DIR, "HelveticaRegular.ttf"),
    )
)


def generate_pdf(data):
    """Создание отчета в формате .pdf"""

    buffer = BytesIO()
    report = SimpleDocTemplate(buffer, pagesize=landscape(A4))

    styles = getSampleStyleSheet()
    header_style = styles["Heading2"]

    elements = []

    header = Paragraph(f"Отзывы, {datetime.now()}", header_style)
    elements.append(header)

    table_header = TABLE_HEADER.copy()
    table_content = [
        map(
            str,
            [
                obj.username,
                obj.userage,
                obj.userhobby,
                obj.exhibit,
                obj.answer_to_message_before_description,
                obj.answer_to_reflection,
                obj.text,
            ],
        )
        for obj in data
    ]
    table_data = [table_header, *table_content]
    table = Table(table_data)
    table.setStyle(
        TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.dimgrey)])
    )
    elements.append(table)

    report.build(elements)
    buffer.seek(0)
    return buffer
