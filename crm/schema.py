#!/usr/bin/env python3
"""

import graphene
crm/schema.py
This file contains the schema configuration for the GraphQL CRM application.
"""

import datetime
from decimal import Decimal

import re
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from crm.models import Customer, Product, Order
from crm.filters import CustomerFilter, ProductFilter, OrderFilter


class CustomerType(DjangoObjectType):
    """
    GraphQL type for the Customer model.
    This class defines the fields available in the Customer type.
    """

    class Meta:
        """Meta class for the CustomerType."""

        model = Customer
        filterset_class = CustomerFilter
        interfaces = (relay.Node,)


class CustomerInput(graphene.InputObjectType):
    """Input type for customer data in mutations."""

    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class CreateCustomer(graphene.Mutation):
    """
    Mutation class for creating a new customer.
    """

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        """arguments for the customer mutation"""

        input = CustomerInput(required=True)

    def mutate(self, info, input):
        """create a new customer in the CRM system."""

        name = input.name
        email = input.email
        phone = input.phone

        if not name or not email:
            return CreateCustomer(customer=None, message="Name and email are required.")

        if Customer.objects.filter(name=name).exists():
            return CreateCustomer(
                customer=None, message=f"Customer with name {name} already exists."
            )

        if Customer.objects.filter(email=email).exists():
            return CreateCustomer(
                customer=None, message=f"Customer with email {email} already exists."
            )

        if phone and not re.match(r"^(\+?\d{10}|\d{3}-\d{3}-\d{4})$", phone):
            return CreateCustomer(
                customer=None,
                message="Phone number is not valid. It should be in the format +1234567890 or 123-456-7890.",
            )

        try:
            customer = Customer.objects.create(name=name, email=email, phone=phone)
            return CreateCustomer(
                customer=customer, message=f"Customer {name} created successfully."
            )
        except Exception as e:
            return CreateCustomer(customer=None, message=str(e))


class DeleteCustomer(graphene.Mutation):
    """
    Mutation class for deleting a customer.
    """

    success = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        """Arguments for the delete customer mutation."""

        customer_id = graphene.ID(required=True)

    def mutate(self, info, customer_id):
        """Delete a customer from the CRM system."""
        try:
            customer = Customer.objects.get(id=customer_id)
            customer.delete()
            return DeleteCustomer(
                success=True, message="Customer deleted successfully."
            )
        except Customer.DoesNotExist:
            return DeleteCustomer(
                success=False, message=f"Customer with ID {customer_id} does not exist."
            )
        except Exception as e:
            return DeleteCustomer(success=False, message=str(e))


class BulkCreateCustomers(graphene.Mutation):
    """
    Mutation class for bulk creating customers.
    """

    errors = graphene.List(graphene.String)
    customers = graphene.List(CustomerType)

    class Arguments:
        """Arguments for the bulk create customers mutation."""

        input = graphene.List(CustomerInput, required=True)

    def mutate(self, info, input) -> "BulkCreateCustomers":
        """Bulk create customers in the CRM system."""
        if not input:
            return BulkCreateCustomers(
                customers=[], errors=["No customer data provided for bulk creation."]
            )

        customers = []
        error_messages = []

        for data in input:
            try:
                result = CreateCustomer().mutate(info, data)

                if result.customer:
                    customers.append(result.customer)
                else:
                    error_messages.append(result.message)

            except Exception as e:
                error_messages.append(str(e))

        return BulkCreateCustomers(customers=customers, errors=error_messages)


class ProductType(DjangoObjectType):
    """
    GraphQL type for the Product model.
    """

    class Meta:
        """Meta class for the ProductType."""

        model = Product
        fields = "__all__"
        filterset_class = ProductFilter
        interfaces = (relay.Node,)


class ProductInput(graphene.InputObjectType):
    """Input type for product data in mutations."""

    name = graphene.String(required=True)
    price = graphene.Float(required=True)
    stock = graphene.Int(default_value=0)


class CreateProduct(graphene.Mutation):
    """Mutation class for creating a new product."""

    product = graphene.Field(ProductType)
    message = graphene.String()

    class Arguments:
        """Arguments for the create product mutation."""

        input = ProductInput(required=True)

    def mutate(self, info, input):
        """Create a new product in the CRM system."""
        name = input.name
        price = Decimal(input.price).quantize(Decimal("0.01"), rounding="ROUND_UP")
        stock = input.stock

        if not name or not price:
            return CreateProduct(product=None, message="Name and price are required.")

        if price < 0:
            return CreateProduct(product=None, message="Price cannot be negative.")

        if stock < 0:
            return CreateProduct(product=None, message="Stock cannot be negative.")

        if Product.objects.filter(name=name).exists():
            return CreateProduct(
                product=None, message=f"Product with name {name} already exists."
            )

        try:
            product = Product.objects.create(name=name, price=price, stock=stock)
            return CreateProduct(
                product=product, message=f"Product {product.name} created successfully."
            )
        except Exception as e:
            return CreateProduct(product=None, message=str(e))


class UpdateLowStockProducts(graphene.Mutation):
    """
    Mutation class for updating low stock products.
    This mutation can be used to update the stock levels of products that are low in inventory.
    """

    success = graphene.Boolean()
    message = graphene.String()
    products = graphene.List(ProductType)

    def mutate(self, info):
        """Update low stock products in the CRM system."""
        try:
            low_stock_products = Product.objects.filter(stock__lt=10)
            for product in low_stock_products:
                product.stock += 10  # Example logic to increase stock
                product.save()

            return UpdateLowStockProducts(
                success=True,
                message="Low stock products updated successfully.",
                products=low_stock_products,
            )
        except ValueError as e:
            return UpdateLowStockProducts(
                success=False,
                message=f"Error updating low stock products: {str(e)}",
                products=None,
            )


class OrderType(DjangoObjectType):
    """
    GraphQL type for the Order model.
    """

    class Meta:
        """Meta class for the OrderType."""

        model = Order
        fields = "__all__"
        filterset_class = OrderFilter
        interfaces = (relay.Node,)


class OrderInput(graphene.InputObjectType):
    """Input type for order data in mutations."""

    customerId = graphene.ID(required=True)
    productIds = graphene.List(graphene.ID, required=True)


class CreateOrder(graphene.Mutation):
    """
    Mutation class for creating a new order.
    """

    order = graphene.Field(OrderType)
    total_amount = graphene.Decimal()
    order_date = graphene.DateTime()

    class Arguments:
        """Arguments for the order mutation."""

        input = OrderInput(required=True)

    def mutate(self, info, input):
        """Create a new order in the CRM system."""
        try:
            customer = Customer.objects.get(id=input.customerId)
        except Customer.DoesNotExist:
            raise ValueError(f"Customer with ID {input.customerId} does not exist.")

        try:
            products = Product.objects.filter(id__in=input.productIds)
        except Product.DoesNotExist:
            raise ValueError("One or more products do not exist.")

        try:
            total_amount = sum(product.price for product in products)
            order_date = datetime.datetime.now()

            order = Order.objects.create(
                customer=customer, order_date=order_date, total_amount=total_amount
            )
            order.products.set(products)

            return CreateOrder(
                order=order,
                total_amount=total_amount,
                order_date=order_date,
            )

        except Exception as e:
            raise ValueError(f"Error creating order: {str(e)}")


class Query(graphene.ObjectType):
    """
    Query class for the CRM application.
    This class defines the queries available in the CRM.
    """

    # Define your queries here
    # all_customers = graphene.List(lambda: CustomerType)
    # all_products = graphene.List(lambda: ProductType)
    # all_orders = graphene.List(lambda: OrderType)

    # def resolve_all_customers(self, info):
    #     """Resolver for the customers query."""
    #     return Customer.objects.all()

    # def resolve_all_products(self, info):
    #     """Resolver for the products query."""
    #     return Product.objects.all()

    # def resolve_all_orders(self, info):
    #     """Resolver for the orders query."""
    #     return Order.objects.all()

    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)

    def resolve_all_customers(self, info, orderby=None, **kwargs):
        """Resolver for the all_customers query."""
        if orderby:
            return Customer.objects.all().order_by(orderby)
        return Customer.objects.all()

    def resolve_all_products(self, info, orderby=None, **kwargs):
        """Resolver for the all_products query."""
        if orderby:
            return Product.objects.all().order_by(orderby)
        return Product.objects.all()

    def resolve_all_orders(self, info, orderby=None, **kwargs):
        """Resolver for the all_orders query."""
        if orderby:
            return Order.objects.all().order_by(orderby)
        return Order.objects.all()


class Mutation(graphene.ObjectType):
    """
    Mutation class for handling create operations in the CRM.
    """

    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()
    delete_customer = DeleteCustomer.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
