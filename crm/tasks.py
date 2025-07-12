"""
CRM Report Generation Task
This module defines a Celery task to generate a weekly CRM report
that summarizes total orders, customers, and revenue, and logs it.
"""

from crm.cron import write_to_log, date
from crm.graphql import BASE_URL

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from celery import shared_task


@shared_task()
def generate_crm_report():
    """
    Logic to generate the CRM report
    """
    log_file = "/tmp/crm_report_log.txt"

    _transport = RequestsHTTPTransport(
        url=BASE_URL,
        verify=True,
        retries=3,
        use_json=True,
    )

    client = Client(transport=_transport, fetch_schema_from_transport=True)

    query = gql(
        """        
        query CRMDashboardStatistics {
            # Get total number of customers
            allCustomers {
                totalCount
            }
            
            # Get total number of orders
            allOrders {
                totalCount
                edges {
                node {
                    totalAmount
                }
                }
            }
        }
        """
    )

    result = client.execute(query)

    if not result:
        write_to_log(log_file, "Failed to generate CRM report.")
    else:
        total_orders = result.get("totalOrders", 0)
        total_customers = result.get("totalCustomers", 0)
        total_revenue = result.get("totalRevenue", 0)

        message = f"{date} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue"
        write_to_log(log_file, message)
