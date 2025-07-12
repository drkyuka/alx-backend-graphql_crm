"""
Configure a Celery task with Celery Beat to generate a weekly CRM report
(summarizing total orders, customers, and revenue) and log it,
integrating with the GraphQL schema.
"""

import os
from celery import Celery


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

app = Celery("crm")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(["crm.tasks"])


@app.task(bind=True)
def debug_task(self):
    """
    Debug task to print the request information.
    """
    print(f"Request: {self.request!r}")
