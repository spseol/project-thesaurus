# Project Thesaurus
System used fo publication, evidence and managing theses and attachments to them. 

## Structure
Project is using docker-compose to compose all required Docker containers to run:
- `web` main container with installed Django
- `db` container with running PostgreSQL database used mainly by Django
- `webpack` utility container containing webpack for build process of frontend assets
- `nginx` container with Nginx to proxy to `web` and serving static files (collected from Django and built by Webpack)

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