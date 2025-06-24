#!/bin/env python3

# -*- coding: utf-8 -*-
"""
alx-backend-graphql_crm.schema.py
This file contains the schema configuration for the GraphQL CRM application.
"""

import graphene
from graphene_django.types import DjangoObjectType
from crm.models import Customer


class CustomerType(DjangoObjectType):
    """
    GraphQL type for the Customer model.
    """

    class Meta:
        """Meta class to define the model for this type."""

        model = Customer
        fields = '__all__'


class Query(graphene.ObjectType):
    """
    The root query for the GraphQL schema.
    This is where you define your queries.
    """

    hello = graphene.String(default_value="Hello, GraphQL!")
    all_customers = graphene.List(CustomerType)
    get_customer = graphene.Field(CustomerType, id=graphene.Int(required=True)))

    def resolve_all_customers(self, info):
        """
        Resolver for the all_customers query.
        Returns a list of all customers in the CRM.
        """
        return Customer.objects.all()


    def resolve_get_customer(self, info, id):
        """
        Resolver for the get_customer query.
        Returns a single customer by ID.
        """

        try:
            return Customer.objects.get(customer_id=id)
        except Customer.DoesNotExist:
            return None

# Create the schema instance that Django will import
schema = graphene.Schema(query=Query)


class CreateCustomer(graphene.Mutation):
    """
    Cbject to create a new customer.
    """

    class Arguments:
        """Arguments for the mutation to create a customer."""

        id = graphene.ID()
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    status = graphene.Boolean()
    message = graphene.String()


    def mutate(self, root, info, name, email, phone=None, id=None):
        """Create a new customer with the provided details."""

        # *** create a new customer instance
        try:
            if not id:
                customer = Customer(name=name, email=email, phone=phone)
                customer.save()
                return CreateCustomer(
                    customer=customer,
                    status=True,
                    message="Customer created successfully."
                )
            
            # check if email exists
            if Customer.objects.filter(email=email).exists():
                return CreateCustomer(
                    customer=None,
                    status=False,
                    message="Email already exists."
                )
  
        

        # *** update a customer instance
            new_customer = Customer.objects.get(customer_id=customer.customer_id)
            new_customer.name = name
            new_customer.email = email
            new_customer.phone = phone
            new_customer.save()
            return CreateCustomer(
                customer=new_customer
                status=True,
                message="Customer updated successfully."
            )
          
        except Exception as e:
            return CreateCustomer(
                customer=None,
                status=False,
                message=f"An error occurred: {str(e)}"
            )

class BulkCreateCustomers(graphene.Mutation):
    """
    Mutation to create multiple customers at once.
    """

    class Arguments:
        """Arguments for the mutation to create multiple customers."""

        customers = graphene.List(CustomerType, required=True)

    errors = graphene.List(graphene.String)

    def mutate(self, root, info, customers):
        """Create multiple customers with the provided details."""

        errors = []
        created_customers = []

        try:
            for customer_data in customers:
                customer = CreateCustomer().mutate(
                    root, info, 
                    name=customer_data.get('name'),
                    email=customer_data.get('email'),
                    phone=customer_data.get('phone', None)
                )

                # Check if the customer was created successfully
                if customer and customer.status:
                    created_customers.append(customer)
                else:
                    errors.append(customer.message)

            return BulkCreateCustomers(
                errors=errors,
                customers=created_customers
            )
        
        except Exception as e:
            errors.append(f"An error occurred: {str(e)}")
            return BulkCreateCustomers(
                errors=errors,
                customers=[]
            )

class Mutation(graphene.ObjectType):
    """
    The root mutation for the GraphQL schema.
    """

    create_customer = CreateCustomer.Field()
    update_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()


# Create the schema instance that Django will import
schema = graphene.Schema(query=Query, mutation=Mutation)
