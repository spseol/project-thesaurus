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
- [`web`](https://hub.docker.com/r/thejoeejoee/thesaurus-django) main container with installed Django 
[![](https://images.microbadger.com/badges/version/thejoeejoee/thesaurus-django.svg)](https://microbadger.com/images/thejoeejoee/thesaurus-django)

- `db` container with running PostgreSQL database used mainly by Django 

- [`webpack`](https://hub.docker.com/r/thejoeejoee/thesaurus-webpack) utility container containing webpack for build process of frontend assets [![](https://images.microbadger.com/badges/version/thejoeejoee/thesaurus-webpack.svg)](https://microbadger.com/images/thejoeejoee/thesaurus-webpack)

- [`webserver`](https://hub.docker.com/r/thejoeejoee/thesaurus-nginx) container with Nginx to proxy to `web` and serving static files (collected from Django and built by Webpack) [![](https://images.microbadger.com/badges/version/thejoeejoee/thesaurus-nginx.svg)](https://microbadger.com/images/thejoeejoee/thesaurus-nginx)

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
- Python 3.8
- Django 3.0
- Webpack 4.42
- Nginx 1.17.4
- PostgreSQL 12.0

## License
This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.
