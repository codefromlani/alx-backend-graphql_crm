# CRM Celery Setup Guide

## 1. Install Redis and dependencies

```bash
sudo apt install redis-server
redis-server --daemonize yes
pip install -r requirements.txt
```
## 2. Run migrations

```bash
python manage.py migrate
```
## 3. Start Celery worker

```bash
celery -A crm worker -l info
```
## 4. Start Celery Beat scheduler

```bash
celery -A crm beat -l info
```
## 5. Verify the log

```bash
cat /tmp/crm_report_log.txt
```
Each Monday at 6 AM, a new line should appear with:
```bash
YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue
```

## 6: Verify setup works

Run the worker and beat locally for testing:
```bash
celery -A crm worker -l info
celery -A crm beat -l info
```

Then manually trigger the task in Django shell:
```bash
python manage.py shell
```
```bash
from crm.tasks import generate_crm_report
generate_crm_report.delay()
```

Then Check:
```bash
cat /tmp/crm_report_log.txt
```
