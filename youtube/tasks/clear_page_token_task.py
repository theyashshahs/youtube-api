import logging
from datetime import timedelta
from os import path, remove

from celery.decorators import periodic_task
from django.conf import settings

logger = logging.getLogger(__name__)

# Aysnc task to clear the page token
@periodic_task(
    # runs every 2 minutes
    run_every=timedelta(minutes=2),
    name="clear_page_token",
    ignore_result=True,
)
def clear_page_token():
    # Check if the file exists
    if path.exists(path.join(settings.BASE_DIR, "next_page_token.txt")):
        # Delete the file
        remove(path.join(settings.BASE_DIR, "next_page_token.txt"))
        logger.info("Successfully cleared the page token")
