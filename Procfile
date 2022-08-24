release: python manage.py migrate
web: gunicorn gaalguimoney.wsgi
celeryworker2: celery -A gaalguimoney.celery worker & celery -A gaalguimoney beat -l INFO & wait -n