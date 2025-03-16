import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "farma.settings")

app = Celery("farma")

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()


app.conf.beat_schedule = {
    "check_medicine_expiry": {
        "task": "check_medicine_expiry",
        "schedule": crontab(minute=0, hour=0),
    },
}
