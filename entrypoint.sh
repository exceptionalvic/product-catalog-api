#!/bin/sh

set -e

# Run Migrations
if [ "x$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
    echo "migration successful"
fi

# Run collectstatic
if [ "x$DJANGO_MANAGEPY_COLLECTSTATIC" = 'xon' ]; then
    python manage.py collectstatic --no-input;
    echo "collectstatic ran successfully"
fi

# Create superuser
if [ "x$DJANGO_MANAGEPY_CREATE_SUPERUSER" = 'xon' ]; then
    python manage.py create_super_user;
    echo "superuser created successfully"
fi

exec "$@"
