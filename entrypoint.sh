#!/bin/bash

# Aplicar migraciones
python manage.py makemigrations
python manage.py migrate

# Crear tabla de caché
python manage.py createcachetable

# Crear superusuario si se proporcionan las variables de entorno
if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ] && [ "$DJANGO_SUPERUSER_EMAIL" ]
then
    python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
fi

# Ejecutar cualquier otro comando proporcionado como argumento
exec "$@"
