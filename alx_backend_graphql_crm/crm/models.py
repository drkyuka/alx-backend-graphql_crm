"""crm/models.py
This file contains the models for the CRM application.
"""

from django.db import models


class Customer(models.Model):
    """
    Model to represent a customer in the CRM system.
    """

    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer {self.name}, Email: {self.email}, Phone: {self.phone}"
