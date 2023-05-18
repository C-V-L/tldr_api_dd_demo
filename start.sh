python manage.py migrate --no-input
gunicorn tldr_api.wsgi:application --bind 0.0.0.0:10000 --timeout 120