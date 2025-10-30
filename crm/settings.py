from django.conf import settings

DEBUG = True
INSTALLED_APPS = getattr(settings, "INSTALLED_APPS", []) + ["django_crontab", 'crm',]

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]

