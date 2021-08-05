from django.db import models


class Youtube(models.Model):
    video_id = models.CharField(max_length=50, blank=False, unique=True)
    title = models.CharField(max_length=150, blank=False)
    description = models.CharField(max_length=1000, blank=True)
    thumbnails = models.JSONField(null=True, blank=True)
    published_at = models.DateTimeField(blank=False)

    def __str__(self):
        return self.title
