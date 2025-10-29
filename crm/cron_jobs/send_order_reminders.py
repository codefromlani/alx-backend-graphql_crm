#!/usr/bin/env python3
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import datetime

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate date 7 days ago
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat()

# Define query
query = gql(f"""
query {{
  allOrders(filter: {{ orderDateGte: "{seven_days_ago}" }}) {{
    edges {{
      node {{
        id
        orderDate
        customer {{
          email
        }}
      }}
    }}
  }}
}}
""")

# Execute query
result = client.execute(query)

# Log to file
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a") as f:
    f.write(f"\n[{timestamp}] Order reminders run:\n")
    if result and "allOrders" in result:
        for edge in result["allOrders"]["edges"]:
            order = edge["node"]
            f.write(f"Order ID: {order['id']} - Customer Email: {order['customer']['email']}\n")
    else:
        f.write("No recent orders found or query failed.\n")

print("Order reminders processed!")
