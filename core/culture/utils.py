import os
from datetime import datetime
from io import BytesIO

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build
from PIL import Image, ImageOps
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

    content = [
        map(
            str,
            [
                review.username,
                review.userage,
                review.userhobby,
                review.exhibit,
                review.answer_to_message_before_description,
                review.answer_to_reflection,
                review.text,
            ],
        )
        for review in data
    ]
    table_data = [TABLE_HEADER.copy(), *content]
    table = Table(table_data)
    table.setStyle(
        TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.dimgrey)])
    )
    elements.append(table)

    report.build(elements)
    buffer.seek(0)
    return buffer


def update_spreadsheet(reviews):
    """Экспорт данных в существующий файл Google Spreadsheets"""

    credentials = None
    credentials = service_account.Credentials.from_service_account_info(
        info=settings.SPREADSHEETS_INFO, scopes=settings.SPREADSHEETS_SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    content = [
        [
            review.username,
            review.userage,
            review.userhobby,
            str(review.exhibit),
            review.answer_to_message_before_description,
            review.answer_to_reflection,
            review.text,
        ]
        for review in reviews
    ]
    data = [TABLE_HEADER.copy(), *content]

    sheet.values().clear(
        spreadsheetId=settings.SPREADSHEET_ID, range="A1:G1"
    ).execute()
    sheet.values().append(
        spreadsheetId=settings.SPREADSHEET_ID,
        range="A1:G1",
        valueInputOption="USER_ENTERED",
        body={"values": data},
    ).execute()


def prepare_image(image, filepath):
    """Обработка изображения перед сохранением в базу данных"""

    img = Image.open(image)
    fixed_width = 1080
    img = Image.open(filepath)
    img = ImageOps.exif_transpose(img)
    width_percent = fixed_width / float(img.size[0])
    height_size = int((float(img.size[1]) * float(width_percent)))
    new_image = img.resize((fixed_width, height_size))
    if new_image.format != "JPEG":
        new_image = new_image.convert("RGB")
    new_image.save(filepath, "JPEG")
