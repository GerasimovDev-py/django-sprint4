FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY blogicum/ /app/

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "blogicum.wsgi:application", "--bind", "0.0.0.0:8000"]