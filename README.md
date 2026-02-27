# Project Thesaurus [![GitHub license](https://img.shields.io/github/license/spseol/project-thesaurus.svg)](https://github.com/spseol/project-thesaurus/blob/master/LICENSE) [![GitHub release](https://img.shields.io/github/tag/spseol/project-thesaurus.svg)](https://GitHub.com/spseol/project-thesaurus/releases/)


System used fo publication, evidence and managing theses and attachments to them. 



![Made with Python](https://img.shields.io/badge/Made%20with-Python-4584b6.svg)
![Made with Vue.js](https://img.shields.io/badge/Made%20with-Vue.js-42b883.svg)
![Made with Docker](https://img.shields.io/badge/Made%20with-Docker-0db7ed.svg)
![Made with Django](https://img.shields.io/badge/Made%20with-Django-092e20.svg)
![Made with Django](https://img.shields.io/badge/Made%20with-Webpack-8ED5FA.svg)
![Made with Django](https://img.shields.io/badge/Made%20with-PostgreSQL-cc3b03.svg)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/spseol/project-thesaurus.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/spseol/project-thesaurus/context:python)
[![Language grade: JavaScript](https://img.shields.io/lgtm/grade/javascript/g/spseol/project-thesaurus.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/spseol/project-thesaurus/context:javascript)



## Structure
Project is using docker-compose to compose all required Docker containers to run:
- [`web`](https://hub.docker.com/r/thejoeejoee/thesaurus-django) [![](https://images.microbadger.com/badges/version/thejoeejoee/thesaurus-django.svg)](https://microbadger.com/images/thejoeejoee/thesaurus-django) main container with installed Django 

- `db` container with running PostgreSQL database used by Django Models 

- [`webpack`](https://hub.docker.com/r/thejoeejoee/thesaurus-webpack) [![](https://images.microbadger.com/badges/version/thejoeejoee/thesaurus-webpack.svg)](https://microbadger.com/images/thejoeejoee/thesaurus-webpack) utility container containing webpack for build process of frontend assets 

- [`webserver`](https://hub.docker.com/r/thejoeejoee/thesaurus-nginx) [![](https://images.microbadger.com/badges/version/thejoeejoee/thesaurus-nginx.svg)](https://microbadger.com/images/thejoeejoee/thesaurus-nginx) container with Nginx to proxy to `web` and serving static and media files 

## Getting Started

### 1. Environment setup

Copy the env template and fill in the required values:

```bash
cp .env.local.template .env.local
```

Open `.env.local` and set at minimum:

| Variable        | Required | Description                                                                                                 |
|-----------------|----------|-------------------------------------------------------------------------------------------------------------|
| `SECRET_KEY`    | Yes      | Django secret key — generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `ALLOWED_HOSTS` | Yes      | Space-separated hostnames, e.g. `localhost 127.0.0.1`                                                      |
| `PUBLIC_HOST`   | Yes      | Base URL for absolute links, e.g. `http://localhost:8080`                                                   |
| `TZ`            | Yes      | Timezone, e.g. `Europe/Prague`                                                                              |
| `LDAP_HOST`     | No       | Leave empty to disable LDAP auth entirely                                                                   |

> Email vars default to a console backend in dev (`django/.env.dev`).  
> LDAP is **optional** in development — leave `LDAP_HOST` empty to skip it.

### 2. Running locally (Docker)

The root `.env` file sets `COMPOSE_FILE` to the dev stack by default, so plain `docker compose` commands work without any extra flags.

```bash
make build   # build images (first time or after Dockerfile changes)
make up      # start everything, stream logs
make upd     # start as daemons
make down    # stop and remove containers
make logs    # follow logs
```

The app is available at **http://localhost:8080**.  
The webpack dev server (with HMR) runs on **http://localhost:3000**.

> To use a custom hostname for HMR WebSocket URLs, set `SITE_URL=your-hostname` in your shell.

### 3. Shell access & management commands

```bash
make shell-web      # shell into the Django container
make shell-webpack  # shell into the webpack container
make migrate        # run Django migrations
make manage CMD="createsuperuser"  # run any management command
```

### 4. Running webpack locally (without Docker)

Requires Node ≥ 17. The `NODE_OPTIONS` flag is baked into the npm scripts.

```bash
cd webpack
npm install
npm run dev    # starts dev server on :3000
npm run build  # production bundle
```

## Usage

### Production

The production stack uses pre-built images. `IMAGE_VERSION` is derived automatically from the last merged git tag.

```bash
make prod-upd     # start production stack (detached)
make prod-reload  # rebuild webpack + migrate + collectstatic + restart
make prod-down    # stop production stack
```

### Releasing images

```bash
make release-django TAG=1.2.3         # build & push Django image
make retag-nginx FROM=1.2.2 TO=1.2.3  # retag nginx image
```

### Database

```bash
make dump-db   # dump dev DB to ./dump.sql
```

## Build with
- Python 3.9
- Django 3.2
- Webpack 4
- Nginx 1.27
- PostgreSQL 12+

## License
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.
