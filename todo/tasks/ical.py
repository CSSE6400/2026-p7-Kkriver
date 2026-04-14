import datetime
import os
import time

import icalendar
from celery import Celery


celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
celery.conf.task_default_queue = os.environ.get("CELERY_DEFAULT_QUEUE", "ical")


@celery.task(name="ical")
def create_ical(tasks):
    cal = icalendar.Calendar()
    cal.add("prodid", "-//Taskoverflow Calendar//mxm.dk//")
    cal.add("version", "2.0")

    delay_seconds = float(os.environ.get("ICAL_GENERATION_DELAY_SECONDS", "5"))
    if delay_seconds > 0:
        time.sleep(delay_seconds)

    for task in tasks:
        deadline = task.get("deadline_at")
        if not deadline:
            continue

        event = icalendar.Event()
        event.add("uid", str(task["id"]))
        event.add("summary", task["title"])
        event.add("description", task.get("description") or "")
        event.add("dtstart", datetime.datetime.fromisoformat(deadline))
        cal.add_component(event)

    return cal.to_ical().decode("utf-8")
