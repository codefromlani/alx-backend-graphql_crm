import os
from datetime import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from celery import shared_task

@shared_task
def generate_crm_report():
    # Setup GraphQL client
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql/",
        verify=False,
        retries=3,
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    # GraphQL query
    query = gql("""
    query {
        allCustomers {
            totalCount
        }
        allOrders {
            totalCount
        }
    }
    """)

    try:
        result = client.execute(query)

        total_customers = result.get("allCustomers", {}).get("totalCount", 0)
        total_orders = result.get("allOrders", {}).get("totalCount", 0)

        # Calculate total revenue via Django ORM (simpler + safer)
        from crm.models import Order
        total_revenue = sum(o.total_amount for o in Order.objects.all())

        # Log to file
        log_path = "/tmp/crm_report_log.txt"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report_line = f"{timestamp} - Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"

        with open(log_path, "a") as log_file:
            log_file.write(report_line)

        logging.info("CRM report generated successfully.")
    except Exception as e:
        logging.error(f"Error generating CRM report: {e}")
