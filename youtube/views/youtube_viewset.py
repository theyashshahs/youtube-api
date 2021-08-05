from rest_framework import viewsets
from youtube.serializers import YoutubeSerializer
from youtube.models import Youtube


class YoutubeViewSet(viewsets.ModelViewSet):
    queryset = Youtube.objects.all()
    serializer_class = YoutubeSerializer
