import logging
from datetime import datetime, timedelta

from celery.decorators import periodic_task
from service_interfaces.youtube import get_youtube_searches
from youtube.models import Youtube

logger = logging.getLogger(__name__)


@periodic_task(
    run_every=timedelta(seconds=10),
    name="youtube_search",
    ignore_result=True,
)
def youtube_search():
    # Call the youtube search API with params using youtube interface
    published_after = datetime.now() - timedelta(days=1)
    search_param = "cristiano ronaldo"
    data = get_youtube_searches(
        date=published_after.strftime("%Y-%m-%dT%H:%M:%SZ"),
        search_param=search_param,
    )

    if data["status"] == "success":
        logger.info("Successfully retrieved youtube search data")
        results = data["data"]["items"]

        # iterate through the list and create youtube model objects
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
