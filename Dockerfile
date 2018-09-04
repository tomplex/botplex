FROM python:3.6-alpine

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

ENV FLASK_ENV 'production'

COPY . /botplex

ENTRYPOINT ["python", "/botplex/main.py"]
