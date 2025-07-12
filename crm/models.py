"""crm/models.py
This file contains the models for the CRM application.
"""

from django.db import models
from django.core.validators import MinValueValidator


class Customer(models.Model):
    """
    Model to represent a customer in the CRM system.
    """

    objects = models.BaseManager()

    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Customer {self.name}, Email: {self.email}, Phone: {self.phone}"


class Product(models.Model):
    """
    Model to represent a product in the CRM system.
    """

    objects = models.BaseManager()

    name = models.CharField(max_length=255, blank=False, null=False)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        validators=[MinValueValidator(0.00)],
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Product {self.name}, Price: {self.price}, Stock: {self.stock}"


class Order(models.Model):
    """
    Model to represent an order in the CRM system.
    """

    customer = models.ForeignKey(
        Customer, related_name="order_customer", on_delete=models.CASCADE
    )

    products = models.ManyToManyField(
        "Product", related_name="order_products", blank=False
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=False,
        validators=[MinValueValidator(0.00)],
    )

    order_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        products = ", ".join([product.name for product in self.products.all()])
        return f"Order {self.id} for {self.customer.name} - {products}"
