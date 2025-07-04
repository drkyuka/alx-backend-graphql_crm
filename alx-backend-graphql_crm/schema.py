#!/bin/env python3

# -*- coding: utf-8 -*-
"""
graphql_crm/schema.py
alx-backend-graphql_crm schema.py
"""

import graphene
from crm.schema import Query as CRMQuery, Mutation as CRMMutation


class Query(CRMQuery, graphene.ObjectType):
    """Query to return a greeting message."""

    hello = graphene.String(default_value="Hello, GraphQL!")


class Mutation(CRMMutation, graphene.ObjectType):
    """Mutation to handle create operations in the CRM."""

    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
