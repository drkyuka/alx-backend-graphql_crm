#!/usr/bin/env python3
# This script logs a heartbeat message for the CRM system.

import datetime

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


BASE_URL = "http://localhost:8000/graphql"


def write_to_log(message: str):
    """
    Write a message to the log file with a timestamp.
    """
    date = datetime.datetime.now().strftime("%D/%M/%Y-%H:%M:%S")
    log_file = "/tmp/cron_log.txt"

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{date} {message}\n")


def log_crm_heartbeat():
    """
    Log a heartbeat message for the CRM system.
    This function is intended to be run periodically to ensure the CRM system is operational.
    """

    write_to_log("CRM is alive")

    _transport = RequestsHTTPTransport(
        url=BASE_URL,
        verify=True,
        retries=3,
    )

    client: Client = Client(transport=_transport, auto_schema=True)

    query = gql(
        """
        query {
            hello
        }
        """
    )

    # Execute the query to ensure the CRM is responsive
    response = client.execute(query).get("hello", "CRM is not responding")
