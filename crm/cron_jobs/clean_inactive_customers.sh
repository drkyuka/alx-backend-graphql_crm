#!/bin/bash
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
    # for customer in inactive_customers:
    #     customer.delete()

    print(count_inactive)
    "
)

if [ -n "$deleted_customers" ]; then
    echo "$deleted_customers inactive customers deleted since $timestamp" >> /tmp/customer_cleanup_log.txt 2>&1
else
    echo "No inactive customers to delete."
fi