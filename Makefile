# ============================================================
#  project-thesaurus – development & release helpers
#  Default target: dev stack via COMPOSE_FILE in .env
# ============================================================

SHELL := /bin/bash

# --- image release config ---
TAG    ?= latest
IMAGE  ?= thejoeejoee/thesaurus
FROM   ?=
TO     ?=

# --- derive IMAGE_VERSION from the last merged git tag (prod) ---
IMAGE_VERSION ?= $(shell git tag --merged | tail -n1)

# ============================================================
#  Dev workflow
# ============================================================

.PHONY: up upd down build logs shell-web shell-webpack shell-nginx migrate manage

## Start the dev stack (foreground)
up:
	docker compose up

## Start the dev stack (detached)
upd:
	docker compose up -d

## Stop and remove containers
down:
	docker compose down

## Build / rebuild dev images
build:
	docker compose build

## Follow logs (all services, last 50 lines)
logs:
	docker compose logs -f --tail=50

## Open a shell in the web (Django) container
shell-web:
	docker compose exec web /bin/sh

## Open a shell in the webpack container
shell-webpack:
	docker compose exec webpack /bin/sh

## Open a shell in the webserver (nginx) container
shell-nginx:
	docker compose exec webserver /bin/sh

## Run Django migrations inside a temporary web container
migrate:
	docker compose run --rm web migrate

## Run an arbitrary Django management command: make manage CMD="createsuperuser"
manage:
	docker compose run --rm web python manage.py $(CMD)

# ============================================================
#  Production workflow
# ============================================================

.PHONY: prod-up prod-upd prod-down prod-reload

PROD_COMPOSE := COMPOSE_FILE=docker-compose.base.yml:docker-compose.prod.yml IMAGE_VERSION=$(IMAGE_VERSION)

## Start the production stack (foreground)
prod-up:
	$(PROD_COMPOSE) docker compose up

## Start the production stack (detached)
prod-upd:
	$(PROD_COMPOSE) docker compose up -d

## Stop and remove production containers
prod-down:
	$(PROD_COMPOSE) docker compose down

## Reload production: rebuild webpack, run migrations, collect static, restart web
prod-reload:
	$(PROD_COMPOSE) docker compose run --rm webpack build
	$(PROD_COMPOSE) docker compose run --rm web migrate
	$(PROD_COMPOSE) docker compose run --rm web python manage.py collectstatic --noinput
	$(PROD_COMPOSE) docker compose restart web webserver

# ============================================================
#  Image release
# ============================================================

.PHONY: release-django retag-nginx retag-webpack retag

## Build and push the Django image for linux/amd64
release-django:
	docker build --platform linux/amd64 -t $(IMAGE)-django:$(TAG) django/
	docker push $(IMAGE)-django:$(TAG)

## Retag and push the nginx image (FROM=old-tag TO=new-tag)
retag-nginx:
	$(MAKE) retag IMAGE=$(IMAGE)-nginx

## Retag and push the webpack image (FROM=old-tag TO=new-tag)
retag-webpack:
	$(MAKE) retag IMAGE=$(IMAGE)-webpack

## Generic retag helper: pull FROM, tag as TO, push
retag:
	docker pull $(IMAGE):$(FROM)
	docker tag  $(IMAGE):$(FROM) $(IMAGE):$(TO)
	docker push $(IMAGE):$(TO)

# ============================================================
#  Database helpers
# ============================================================

.PHONY: dump-db

## Dump the dev postgres database to ./dump.sql
dump-db:
	docker compose exec db pg_dump -U thesaurus thesaurus > dump.sql
