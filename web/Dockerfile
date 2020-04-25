# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN addgroup -S django \
    && adduser -s /bin/sh -D -S -G django django \
    && pip install --upgrade pip \
    && pip install pipenv \
    && apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev gettext-dev \
    && apk add postgresql-dev gettext \
    && pipenv install psycopg2-binary --skip-lock --dev \
    && apk del build-deps \
    && mkdir /usr/src/static \
    && chown django:django /usr/src/static

# install other deps
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system --dev

# copy project
COPY . /usr/src/app/

ENTRYPOINT ["./docker-entrypoint.sh"]
