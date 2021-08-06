import logging
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from django.conf import settings
from service_interfaces.youtube import get_youtube_searches

from youtube.models import Youtube

logger = logging.getLogger(__name__)

PAGE_TOKEN = []

# Async task to get youtube searches and strore them in the database
@periodic_task(
    # runs every 20 seconds
    run_every=timedelta(seconds=20),
    name="youtube_search",
    ignore_result=True,
)
def youtube_search():
    # Call the youtube search API with params using youtube interface
    published_after = datetime.now() - timedelta(days=1)
    search_param = "cristiano ronaldo real madrid juventus"

    # Search parameters
    params = {
        "part": "snippet",
        "q": search_param,
        "key": settings.YOUTUBE_DATA_API_KEY,
        "type": "video",
        "order": "date",
        "publishedAfter": published_after.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "maxResults": 50,
    }

    if PAGE_TOKEN:
        params["pageToken"] = PAGE_TOKEN[0]
        PAGE_TOKEN.pop(0)

    # Get the first page results
    data = get_youtube_searches(params=params)
    if data["status"] == "success":
        logger.info("Successfully retrieved youtube search data")

        # Check for a next page token
        # If there is a next page token, then get the next page token
        # store it into array
        if "nextPageToken" in data["data"]:
            next_page_token = data["data"]["nextPageToken"]
            PAGE_TOKEN.append(next_page_token)

        results = data["data"]["items"]

        # Iterate through the list and create youtube model objects
        for result in results:
            if result["id"]["videoId"] not in Youtube.objects.values_list("video_id", flat=True):
                Youtube.objects.create(
                    video_id=result["id"]["videoId"],
                    published_at=result["snippet"]["publishedAt"],
                    title=result["snippet"]["title"],
                    description=result["snippet"]["description"],
                    thumbnails=result["snippet"]["thumbnails"],
                )
                logger.info("Created Youtube model object")

    # log the errors
    else:
        logger.error("Error retrieving youtube search data")
