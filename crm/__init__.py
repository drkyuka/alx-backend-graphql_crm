"""
Load celery app for the CRM application.
"""

from .celery import app as celery_app

__all__ = ("celery_app",)
