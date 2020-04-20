#!/bin/sh

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
    run "python manage.py collectstatic --noinput && python manage.py runserver_plus --nopin 0.0.0.0:8000"
    ;;
  runserver_prod)
    # runtime under django user
    run "gunicorn thesaurus.wsgi -b 0.0.0.0:8000"
    ;;
  *)
    exec "$@"
    exit
    ;;
esac
