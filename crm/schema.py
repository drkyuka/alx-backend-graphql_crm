"""

import graphene
crm/schema.py
This file contains the schema configuration for the GraphQL CRM application.
"""

import re
import graphene
from graphene_django import DjangoObjectType
from crm.models import Customer, Product, Order
from decimal import Decimal


class CustomerType(DjangoObjectType):
    """
    GraphQL type for the Customer model.
    This class defines the fields available in the Customer type.
    """

    class Meta:
        """Meta class for the CustomerType."""

        model = Customer
        fields = "__all__"


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

        name = input.get("name")
        email = input.get("email")
        phone = input.get("phone")

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

        if phone and not re.match(r"^(\+?\d{7,15}|\d{3}-\d{3}-\d{4})$", phone):
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
        price = Decimal(str(input.price)).quantize(Decimal("0.01"))
        stock = input.stock

        if not name or not price:
            return CreateProduct(product=None, message="Name and price are required.")

        if price < 0:
            return CreateProduct(product=None, message="Price cannot be negative.")

        if stock < 0:
            return CreateProduct(product=None, message="Stock cannot be negative.")

        # if Product.objects.filter(name=name).exists():
        #     return CreateProduct(
        #         product=None, message=f"Product with name {name} already exists."
        #     )

        try:
            product = Product.objects.create(name=name, price=price, stock=stock)
            return CreateProduct(
                product=product, message=f"Product {name} created successfully."
            )
        except Exception as e:
            return CreateProduct(product=None, message=str(e))


class OrderType(DjangoObjectType):
    """
    GraphQL type for the Order model.
    """

    class Meta:
        """Meta class for the OrderType."""

        model = Order
        fields = "__all__"


class CreateOrder(graphene.Mutation):
    """
    Mutation class for creating a new order.
    """

    order = graphene.Field(OrderType)
    total_amount = graphene.Decimal()

    class Arguments:
        """Arguments for the order mutation."""

        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    def mutate(
        self, _info: graphene.ResolveInfo, customer_id: str, product_ids: list
    ) -> "CreateOrder":
        """Create a new order in the CRM system."""
        try:
            customer = Customer.objects.get(id=customer_id)
            products = Product.objects.filter(id__in=product_ids)

            total_amount = sum(product.price for product in products)
            order = Order.objects.create(customer=customer, total_amount=total_amount)
            order.products.set(products)
            return CreateOrder(order=order)

        except Product.DoesNotExist:
            raise ValueError(
                f"One or more products with IDs {product_ids} do not exist."
            )
        except Customer.DoesNotExist:
            raise ValueError(f"Customer with ID {customer_id} does not exist.")
        except Exception as e:
            raise ValueError(f"Error creating order: {str(e)}")


class Query(graphene.ObjectType):
    """
    Query class for the CRM application.
    This class defines the queries available in the CRM.
    """

    # Define your queries here
    customers = graphene.List(lambda: CustomerType)
    products = graphene.List(lambda: ProductType)
    orders = graphene.List(lambda: OrderType)

    def resolve_customers(self, info):
        """Resolver for the customers query."""
        return Customer.objects.all()

    def resolve_products(self, info):
        """Resolver for the products query."""
        return Product.objects.all()

    def resolve_orders(self, info):
        """Resolver for the orders query."""
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
