import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate
from reportlab.platypus.tables import Table, TableStyle, colors

TABLE_HEADER = ["Username", "Возраст", "Текст отзыва"]

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
    report = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    header_style = styles["Heading2"]

    elements = []

    header = Paragraph(f"Отчет на {datetime.now()}", header_style)
    elements.append(header)

    table_header = TABLE_HEADER.copy()
    table_content = [
        map(str, [obj.username, obj.userage, obj.text]) for obj in data
        ]
    table_data = [table_header, *table_content]
    table = Table(table_data)
    table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.aqua)]))
    elements.append(table)

    report.build(elements)
    buffer.seek(0)
    return buffer
