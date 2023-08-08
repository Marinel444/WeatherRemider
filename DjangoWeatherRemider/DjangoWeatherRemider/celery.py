import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoWeatherRemider.settings')
app = Celery('main')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'tasks-check-notification': {
        'task': 'weather.tasks.check_notification',
        'schedule': crontab(minute='*/30'),
        'args': (),
    },
    'tasks-get-city-weather': {
        'task': 'weather.tasks.get_city_weather',
        'schedule': crontab(minute='0', hour='*/3'),
        'args': (),
    },
}
