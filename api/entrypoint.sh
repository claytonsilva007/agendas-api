#!/bin/sh

# Esperar pelo banco de dados
if [ "$DATABASE" = "postgres" ]
then
    echo "Esperando pelo banco de dados..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "Banco de dados PostgreSQL iniciou"
fi

# Fazer as migrações
python manage.py makemigrations
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

exec "$@"
