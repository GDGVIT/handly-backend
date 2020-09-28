FROM python:3.8

RUN mkdir -p /usr/app/
WORKDIR /usr/app

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install psycopg2 psycopg2-binary
RUN pip install -r requirements.txt

COPY . .

CMD python manage.py collectstatic

CMD python manage.py runserver 0.0.0.0:80