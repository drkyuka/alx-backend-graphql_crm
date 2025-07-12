#!/bin/bash

# script deletes inactive customers 

# set the base variable to the directory of this script
base="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cwd=$(pwd)
log_file="/tmp/customer_cleanup_log.txt"

# check if the log file exists
if cd "$base/../.." ; then
    echo "$timestamp: Error reaching base file." >> "$log_file" 2>&1
    exit 1
fi

# check if log file exists
if [ ! -f "$log_file" ]; then
    touch "$log_file"
fi

# Ensure the script is run from the correct directory
timestamp=$(date +"%Y-%m-%d %H:%M:%S")
deleted_customers=$(
    pipenv run python3 manage.py shell -c "
    from crm.models import Customer, Order
    from django.utils import timezone
    from datetime import timedelta

    # Get all customers who have not placed an order in the last 365 days
    active_customers = Customer.objects.filter(
        order_customer__order_date__gte=timezone.now() - timedelta(days=365)
    ).values_list('id', flat=True)

    # Find customers who are not in the active list
    inactive_customers = Customer.objects.exclude(id__in=active_customers)

    count_inactive = inactive_customers.count()

    # Delete inactive customers one by one to handle related objects safely
    for customer in inactive_customers:
        customer.delete()

    print(count_inactive)
    "
)


if [ -n "$deleted_customers" ]; then
    echo "$timestamp: $deleted_customers inactive customers deleted from $cwd" >> "$log_file" 2>&1
else
    echo "$timestamp: No inactive customers to delete." >> "$log_file" 2>&1

fi