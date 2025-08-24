#!/bin/sh

if [ "$POSTGRES_DB" = "home" ]
then
    echo "Ждем postgres..."

    while ! nc -z "db" $POSTGRES_PORT; do
      sleep 0.5
    done

    echo "PostgreSQL запущен"
fi

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures/news/news.json
python manage.py loaddata fixtures/news/topic.json

exec "$@"