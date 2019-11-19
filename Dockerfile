# pull official base image
FROM python:3.7.4-alpine

RUN mkdir /code
# set work directory
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*

RUN apk add gcc musl-dev python3-dev libffi-dev openssl-dev
RUN apk add --no-cache jpeg-dev zlib-dev

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
# install dependencies
ADD requirements.txt /code/
RUN pip install cryptography numpy Pillow
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./entrypoint.sh /code/entrypoint.sh

# copy project
ADD . /code/

ENTRYPOINT ["/code/entrypoint.sh"]
