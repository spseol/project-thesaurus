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

| Variable       | Required | Description                             |
|----------------|----------|-----------------------------------------|
| `SECRET_KEY`   | Yes      | Django secret key — generate with `python -c "import secrets; print(secrets.token_urlsafe(50))"` |
| `ALLOWED_HOSTS`| Yes      | Space-separated hostnames, e.g. `localhost 127.0.0.1` |
| `PUBLIC_HOST`  | Yes      | Base URL for absolute links, e.g. `http://localhost:8080` |
| `TZ`           | Yes      | Timezone, e.g. `Europe/Prague`          |
| `LDAP_HOST`    | No       | Leave empty to disable LDAP auth entirely |

> Email vars default to a console backend in dev (`django/.env.dev`).
> LDAP is **optional** in development — leave `LDAP_HOST` empty to skip it.

### 2. Running locally (Docker)

The `./run` wrapper sets the correct `COMPOSE_FILE` automatically.

```bash
# Build images (first time only or after Dockerfile changes)
./run dc build

# Start everything and stream logs
./run up

# Or start as daemons
./run upd
```

The app is available at **http://localhost:8080**.  
The webpack dev server (with HMR) runs on **http://localhost:3000**.

> To change the hostname used in HMR WebSocket URLs, set `SITE_URL=your-hostname` in your shell before running.

### 3. Running webpack locally (without Docker)

Requires Node ≥ 17. The `NODE_OPTIONS` flag is baked into the npm scripts.

```bash
cd webpack
npm install
npm run dev    # starts dev server on :3000
npm run build  # production bundle
```

### 4. Applying database migrations

```bash
./run dc run --rm web migrate
```

## Usage
Assuming installed and running Docker, most frequent commands are grouped in script `run`.
For all commands run `$ ./run help`.

Build all needed images:
```bash
$ ./run dc build
```

Start project and watch logs directly in console
```bash
$ ./run up
```

Start project as deamons
```bash
$ ./run upd
```

Successfully started containers exposing port `:8080` on `localhost` with running project.

##### Production

```bash
$ ./run prod up
```

## Build with
- Python 3.9
- Django 3.2
- Webpack 4
- Nginx 1.27
- PostgreSQL 12+

## License
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.
