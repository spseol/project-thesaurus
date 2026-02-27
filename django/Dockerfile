FROM python:3.9.19-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Prague

# Copy uv binary from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/usr/local

# configure users, dirs, install runtime deps
RUN addgroup -S django \
    && adduser -s /bin/sh -D -S -G django django \
    && apk update \
    && apk add --virtual build-deps gcc g++ python3-dev musl-dev gettext-dev jpeg-dev zlib-dev libffi-dev build-base cairo-dev cairo-tools freetype-dev lcms2-dev tiff-dev tk-dev tcl-dev \
    && apk add postgresql-dev gettext cairo-dev pango-dev gdk-pixbuf openjpeg-dev font-noto tzdata \
    && mkdir /usr/src/static /usr/src/media \
    && chown django:django /usr/src/static \
    && chown django:django /usr/src/media \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python deps
COPY ./pyproject.toml ./uv.lock /usr/src/app/
RUN uv sync --frozen --no-cache --no-install-project \
    && apk del build-deps

# copy project
COPY ./ /usr/src/app/

ENTRYPOINT ["./boot.sh", "--", "./docker-entrypoint.sh"]
