import requests
from datetime import datetime

def log_crm_heartbeat():
    log_file = "/tmp/crm_heartbeat_log.txt"
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    graphql_url = "http://localhost:8000/graphql"

    try:
        response = requests.post(
            graphql_url,
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            data = response.json()
            message = f"{timestamp} CRM is alive (GraphQL OK: {data.get('data', {}).get('hello', '')})"
        else:
            message = f"{timestamp} CRM is alive (GraphQL FAILED - HTTP {response.status_code})"
    except Exception as e:
        message = f"{timestamp} CRM is alive (GraphQL ERROR: {e})"

    with open(log_file, "a") as f:
        f.write(message + "\n")
