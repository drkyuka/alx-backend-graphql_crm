#!/usr/bin/env python3
# Create a Python script that uses a GraphQL query
# to find pending orders (order_date within the last week
# )and logs reminders, scheduled to run daily using a cron job.

from datetime import datetime, timedelta
import time
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

BASE_URL = "http://localhost:8000/graphql"


def get_pending_orders():
    """
    Fetch pending orders from the CRM system.
    Returns a list of orders placed within the last week.
    """
    _transport = RequestsHTTPTransport(
        url=BASE_URL,
        use_json=True,
    )
    client = Client(transport=_transport, auto_schema=True)

    query = gql(
        """
        query RecentOrders($lastWeek: DateTime!) {
            allOrders(orderDate_Gte: $lastWeek) {
                edges {
                    node {
                        id
                        customer {
                            email
                        }
                    }
                }
            }
        }
    """
    )

    one_week_ago = datetime.now() - timedelta(days=7)
    variables = {"lastWeek": one_week_ago}

    result = client.execute(query, variable_values=variables)
    return result.get("orders", [])


def process_pending_orders(orders):
    """
    Process the pending orders and log reminders.
    This function simulates sending reminders to customers.
    """
    timestamp = time.time()
    log_file = "/tmp/order_reminders_log.txt"

    with open(log_file, "a", encoding="utf-8") as f:
        for order in orders:
            f.write(
                f"{timestamp}: Reminder sent to {order['customer']['email']} for order {order['id']}\n"
            )


if __name__ == "__main__":
    result = get_pending_orders()
    if result:
        try:
            process_pending_orders(result)
            print("Order reminders processed!")
        except Exception as e:
            print(f"Error processing pending orders: {e}")
    else:
        print("No pending orders found.")
