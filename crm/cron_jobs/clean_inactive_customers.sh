#!/bin/bash
# Deletes customers with no orders for over a year and logs the result

timestamp=$(date "+%Y-%m-%d %H:%M:%S")

deleted_count=$(python3 manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff_date = timezone.now() - timedelta(days=365)
inactive_customers = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff_date)
count = inactive_customers.count()
inactive_customers.delete()
print(count)
EOF
)

echo "\$timestamp - Deleted \$deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
