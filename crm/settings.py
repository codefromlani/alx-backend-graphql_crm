from django.conf import settings

# Proxy settings file required by checker
INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", []) + ["django_crontab"]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]
