#!/bin/env python3

# -*- coding: utf-8 -*-
"""
alx_backend_graphql schema.py
"""

import graphene


class Query(graphene.ObjectType):
    """Query to return a greeting message."""

    hello = graphene.String()

    def resolve_hello(self, info):
        """
        Resolver for the base query.
        """
        return "Hello, GraphQL!"


schema = graphene.Schema(query=Query)
