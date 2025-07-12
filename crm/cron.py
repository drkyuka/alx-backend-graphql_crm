#!/usr/bin/env python3
# This script logs a heartbeat message for the CRM system.

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


BASE_URL = "http://localhost:8000/graphql"


def write_to_log(log_path: str, message: str):
    """
    Write a message to the log file with a timestamp.
    """
    date = datetime.datetime.now().strftime("%D/%M/%Y-%H:%M:%S")

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"{date} {message}\n")


def log_crm_heartbeat():
    """
    Log a heartbeat message for the CRM system.
    This function is intended to be run periodically to ensure the CRM system is operational.
    """
    log_file = "/tmp/crm_heartbeat_log.txt"

    write_to_log(log_file, "CRM is alive")

    _transport = RequestsHTTPTransport(
        url=BASE_URL,
        verify=True,
        retries=3,
    )

    client = Client(transport=_transport, fetch_schema_from_transport=True)

    query = gql(
        """
        query {
            hello
        }
        """
    )

    # Execute the query to ensure the CRM is responsive
    response = client.execute(query).get("hello", "CRM is not responding")

    write_to_log(log_file, f"Response from CRM: {response}")


def update_low_stock():
    """
    Update the stock levels for low inventory items.
    This function is intended to be run periodically to ensure stock levels are accurate.
    """
    log_file = "/tmp/low_stock_updates_log.txt"

    _transport = RequestsHTTPTransport(
        url=BASE_URL,
        verify=True,
        retries=3,
        use_json=True,
    )

    client = Client(transport=_transport, fetch_schema_from_transport=True)
    query = gql(
        """
        mutation {
            updateLowStock {
                success
                message
                products {
                    name
                    stock
                }
            }
        }
        """
    )

    result = client.execute(query)

    if not result:
        write_to_log(log_file, "Failed to update low stock products.")
    else:
        success = result.get("updateLowStock", {}).get("success", False)
        message = result.get("updateLowStock", {}).get("message", "No message provided")
        products = result.get("updateLowStock", {}).get("products", [])

        write_to_log(
            log_file, f"Low stock update success: {success}, Message: {message}"
        )

        if products:
            for product in products:
                name = product.get("name", "Unknown")
                stock = product.get("stock", 0)
                write_to_log(log_file, f"Product: {name}, Updated Stock: {stock}")
        else:
            write_to_log(log_file, "No products updated.")
