from datetime import datetime
from io import BytesIO

from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


styles = getSampleStyleSheet()

def generate_pdf(data):
    """Создание отчета в формате .pdf"""
    
    buffer = BytesIO()
    report = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]

    elements = []
    header = Paragraph(f'Отчет на {datetime.now()}', header_style)
    elements.append(header)

    ...

    report.build(elements)
    buffer.seek(0)
    return FileResponse(
        buffer, as_attachment=True, filename="shopping_list.pdf"
    )
