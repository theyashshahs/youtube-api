import logging
from datetime import datetime, timedelta
from os import path

from celery.decorators import periodic_task
from django.conf import settings
from service_interfaces.youtube import get_youtube_searches

from youtube.models import Youtube

logger = logging.getLogger(__name__)


keys: str = settings.YOUTUBE_DATA_API_KEY

# Generator function to get YOUTUBE API KEY is quota is exceeded
def get_youtube_api_key() -> str:
    keys: list = keys.split(",")[1:]
    for key in keys:
        yield key.strip()


def get_first_youtube_api_key() -> str:
    return (keys.split(",")[0]).strip()


# Async task to get youtube searches and store them in the database
@periodic_task(
    # runs every 20 seconds
    run_every=timedelta(seconds=20),
    name="youtube_search",
    ignore_result=True,
)
def youtube_search():
    # Get the youtube api key
    youtube_api_key = get_youtube_api_key()

    # Call the youtube search API with params using youtube interface
    published_after = datetime.now() - timedelta(days=30)
    search_param: str = "cristiano ronaldo real madrid juventus manchester united"

    youtube_object_list: list = []

    # Check the API KEY
    # Get the key from file if exists
    key: str = ""
    if path.exists(path.join(settings.BASE_DIR, "next_api_key.txt")):
        with open(path.join(settings.BASE_DIR, "next_api_key.txt"), "r") as f:
            key: str = f.read()

    # Search parameters
    params: dict = {
        "part": "snippet",
        "q": search_param,
        "key": key if key else get_first_youtube_api_key(),
        "type": "video",
        "order": "date",
        "publishedAfter": published_after.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "maxResults": 50,
    }

    # Get the token from the file if exists
    if path.exists(path.join(settings.BASE_DIR, "next_page_token.txt")):
        with open(path.join(settings.BASE_DIR, "next_page_token.txt"), "r") as f:
            page_token = f.read()
            if page_token:
                params["pageToken"] = page_token

    # Get page results
    data = get_youtube_searches(params=params)
    if data["status"] == "success":
        logger.info("Successfully retrieved youtube search data")
        # Check for a next page token
        # If there is a next page token, then get the next page token
        if "nextPageToken" in data["data"]:
            next_page_token = data["data"]["nextPageToken"]

            # Save the token in a file
            with open(path.join(settings.BASE_DIR, "next_page_token.txt"), "w") as f:
                f.write(next_page_token)
                f.close()

        results = data["data"]["items"]
        # Iterate through the list and create youtube model objects
        for result in results:
            if result["id"]["videoId"] not in Youtube.objects.values_list("video_id", flat=True):
                obj = Youtube(
                    video_id=result["id"]["videoId"],
                    published_at=result["snippet"]["publishedAt"],
                    title=result["snippet"]["title"],
                    description=result["snippet"]["description"],
                    thumbnails=result["snippet"]["thumbnails"],
                )
                youtube_object_list.append(obj)

    # log the errors and change the API KEY
    else:
        logger.error("Error retrieving youtube search data", data["data"])
        # Change the API key and write it to a file
        with open(path.join(settings.BASE_DIR, "next_api_key.txt"), "w") as f:
            try:
                key = next(youtube_api_key)
                if key:
                    f.write(key)
                else:
                    f.write(get_first_youtube_api_key())
            except StopIteration:
                # If the API key is exhausted, then write the first key to the file
                f.write(get_first_youtube_api_key())
            f.close()

    # Save the youtube model objects
    Youtube.objects.bulk_create(youtube_object_list)
    logger.info("Created %s youtube model objects" % len(youtube_object_list))
