import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    """Run GraphQL mutation to restock low-stock products and log results."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/low_stock_updates_log.txt"

    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    products {
                        name
                        stock
                    }
                    message
                }
            }
        """)
        response = client.execute(mutation)
        products = response["updateLowStockProducts"]["products"]
        message = response["updateLowStockProducts"]["message"]

        log_message = f"{timestamp} {message}\n"
        for p in products:
            log_message += f" - {p['name']}: {p['stock']}\n"
    except Exception as e:
        log_message = f"{timestamp} ERROR: {e}\n"

    with open(log_file, "a") as f:
        f.write(log_message)
