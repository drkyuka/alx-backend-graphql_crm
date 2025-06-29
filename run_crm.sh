#!/bin/bash

# Script to seed the database and run the Django CRM system
# This will populate the database with test data and start the development server

echo "==================================================="
echo "Django CRM System with GraphQL API"
echo "==================================================="

# Change to the project directory
cd "$(dirname "$0")"

echo "Seeding database with test data..."
pipenv run python alx_backend_graphql_crm/seed_db.py

echo ""
echo "Starting Django development server..."
echo "GraphQL endpoint will be available at: http://127.0.0.1:8000/graphql/"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

pipenv run python manage.py runserver
