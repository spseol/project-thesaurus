# pull official base image
FROM python:3.8-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Prague
# install uv into system Python (no venv inside container)
ENV UV_SYSTEM_PYTHON=1

# install uv
COPY --from=ghcr.io/astral-sh/uv:0.10.6 /uv /uvx /usr/local/bin/

# configure users, dirs, and install runtime system deps
RUN addgroup -S django \
    && adduser -s /bin/sh -D -S -G django django \
    && apk update \
    && apk add postgresql-dev gettext cairo-dev pango-dev gdk-pixbuf openjpeg-dev font-noto tzdata \
    && mkdir /usr/src/static /usr/src/media \
    && chown django:django /usr/src/static \
    && chown django:django /usr/src/media \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python deps (separate layer for caching)
COPY ./pyproject.toml ./uv.lock /usr/src/app/
RUN apk add --virtual python-deps libffi-dev build-base cairo-dev cairo cairo-tools \
    jpeg-dev zlib-dev freetype-dev lcms2-dev tiff-dev tk-dev tcl-dev \
    && uv sync --frozen \
    && apk del python-deps

# copy project
COPY ./ /usr/src/app/

ENTRYPOINT ["./boot.sh", "--", "./docker-entrypoint.sh"]
