import datetime
import requests
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport


def log_crm_heartbeat():
    """Log CRM heartbeat with optional GraphQL check."""
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_file = "/tmp/crm_heartbeat_log.txt"

    # Try querying GraphQL hello field
    try:
        transport = RequestsHTTPTransport(
            url="http://localhost:8000/graphql/",
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        response = client.execute(query)
        message = f"CRM is alive (GraphQL OK: {response.get('hello', '')})"
    except Exception as e:
        message = f"CRM is alive (GraphQL ERROR: {e})"

    # Append log entry
    with open(log_file, "a") as f:
        f.write(f"{timestamp} {message}\n")
