import requests
import datetime
from celery import shared_task

@shared_task
def generate_crm_report():
    """
    Generate a weekly CRM report by querying the GraphQL endpoint
    and logging total customers, orders, and revenue.
    """
    query = """
    query {
        allCustomers {
            totalCount
        }
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

    try:
        # Send the GraphQL query
        response = requests.post(
            "http://127.0.0.1:8000/graphql",
            json={"query": query},
            timeout=10,
        )

        if response.status_code != 200:
            log_message = f"{datetime.datetime.now()} - FAILED: HTTP {response.status_code}\n"
        else:
            data = response.json().get("data", {})
            total_customers = data.get("allCustomers", {}).get("totalCount", 0)
            orders = data.get("allOrders", {}).get("edges", [])
            total_orders = len(orders)
            total_revenue = sum(order["node"]["totalAmount"] for order in orders if order["node"]["totalAmount"])

            log_message = (
                f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} - "
                f"Report: {total_customers} customers, {total_orders} orders, {total_revenue} revenue\n"
            )

    except Exception as e:
        log_message = f"{datetime.datetime.now()} - ERROR: {str(e)}\n"

    with open("/tmp/crm_report_log.txt", "a") as f:
        f.write(log_message)
