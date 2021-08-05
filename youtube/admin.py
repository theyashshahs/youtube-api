from django.contrib import admin
from youtube.models import Youtube


class YoutubeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "video_id",
        "published_at",
    )
    list_display_links = (
        "id",
        "video_id",
    )
    search_fields = (
        "title",
        "video_id",
    )


admin.site.register(Youtube, YoutubeAdmin)
