FROM python:3.9-slim

RUN apt-get update && apt-get install -y postgresql-client libgdal-dev

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
