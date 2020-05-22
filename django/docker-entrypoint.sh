#!/bin/sh

DOCKER_HOST_IP=$(ip route show | awk '/default/ {print $3}')
export DOCKER_HOST_IP

run() {
  # Start process as unprivileged user
  # Use `exec` to replace original process.
  # This makes it possible for Docker to send signals to the process.
  exec su django -c "$*"
}

case $1 in
  migrate)
    # under root
    python manage.py makemigrations && python manage.py migrate
    ;;
  django-admin)
    run "$*"
    ;;
  runserver)
    # runtime under django user
    run "python manage.py collectstatic --noinput && python manage.py runserver 0.0.0.0:8000"
    # run "python manage.py collectstatic --noinput && python manage.py runserver_plus --nopin 0.0.0.0:8000"
    ;;
  runserver_prod)
    # runtime under django user
    run "python manage.py collectstatic --noinput && gunicorn thesaurus.asgi -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000"
    ;;
  *)
    exec "$@"
    exit
    ;;
esac

