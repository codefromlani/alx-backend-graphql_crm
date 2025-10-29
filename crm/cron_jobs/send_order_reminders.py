#!/usr/bin/env python3
import requests
import datetime
import json

# GraphQL endpoint
GRAPHQL_URL = "http://localhost:8000/graphql"

# Calculate the date 7 days ago
seven_days_ago = (datetime.datetime.now() - datetime.timedelta(days=7)).date().isoformat()

# GraphQL query to fetch orders within the last 7 days
query = """
query {
  allOrders(filter: { orderDateGte: "%s" }) {
    edges {
      node {
        id
        orderDate
        customer {
          email
        }
      }
    }
  }
}
""" % seven_days_ago

# Send the request
response = requests.post(GRAPHQL_URL, json={'query': query})
data = response.json()

# Log file
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a") as f:
    f.write(f"\n[{timestamp}] Order reminders run:\n")

    if "data" in data and "allOrders" in data["data"]:
        for edge in data["data"]["allOrders"]["edges"]:
            order = edge["node"]
            f.write(f"Order ID: {order['id']} - Customer Email: {order['customer']['email']}\n")
    else:
        f.write("No recent orders found or query failed.\n")

print("Order reminders processed!")
