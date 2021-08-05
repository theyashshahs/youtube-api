from rest_framework import viewsets, pagination
from youtube.serializers import YoutubeSerializer
from youtube.models import Youtube
from apis.utils import paginationTypeByField


class YoutubeViewSet(viewsets.ModelViewSet):
    pagination_class = paginationTypeByField(pagination.CursorPagination, "-published_at")
    queryset = Youtube.objects.all()
    serializer_class = YoutubeSerializer
