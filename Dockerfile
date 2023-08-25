FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r /app/requirements.txt --no-cache-dir
COPY ./ /app
WORKDIR /app/core
CMD ["gunicorn", "core.wsgi:application", "--bind", "0:8000" ]
