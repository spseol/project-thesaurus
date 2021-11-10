# pull official base image
FROM python:3.8.0-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# same for postgres container
ENV TZ Europe/Prague

# configure users, dirs, install psycopg, install runtime deps
RUN addgroup -S django \
    && adduser -s /bin/sh -D -S -G django django \
    && pip install --upgrade pip \
    && pip install pipenv \
    && apk update \
    #   build deps
    && apk add --virtual build-deps gcc g++ python3-dev musl-dev gettext-dev jpeg-dev zlib-dev \
    #  runtime deps
    && apk add postgresql-dev gettext cairo-dev pango-dev gdk-pixbuf openjpeg-dev font-noto tzdata \
    && pipenv install psycopg2-binary --skip-lock --dev \
    && apk del build-deps \
    && mkdir /usr/src/static /usr/src/media \
    && chown django:django /usr/src/static \
    && chown django:django /usr/src/media \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python deps
COPY ./Pipfile ./Pipfile.lock /usr/src/app/
RUN apk add --virtual python-deps libffi-dev build-base cairo-dev cairo cairo-tools \
    jpeg-dev zlib-dev freetype-dev lcms2-dev tiff-dev tk-dev tcl-dev \
    && pipenv install --system --dev \
    && apk del python-deps

# copy project
COPY ./ /usr/src/app/

ENTRYPOINT ["./boot.sh", "--", "./docker-entrypoint.sh"]
