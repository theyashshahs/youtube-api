from apis.utils import _make_query_partial_searchable, paginationTypeByField
from django.contrib.postgres.search import (
    SearchQuery,
    SearchRank,
    SearchVector,
    TrigramSimilarity,
)
from django.db.models import Q
from rest_framework import pagination, viewsets, mixins
from youtube.models import Youtube
from youtube.serializers import YoutubeSerializer


class YoutubeViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    # Pagination class for listing objects based on published_at
    # the minus sign "-" indicates that the published_at field is descending
    pagination_class = paginationTypeByField(pagination.CursorPagination, "-published_at")
    serializer_class = YoutubeSerializer

    def get_queryset(self):
        queryset = Youtube.objects.all()

        # Search by title and description
        search_query = self.request.GET.get("q", None)
        if search_query:
            partial_search_query = SearchQuery(
                _make_query_partial_searchable(search_query), search_type="raw"
            )

            # Create search vector for title and description
            search_vector = SearchVector("title", weight="A") + SearchVector(
                "description", weight="B"
            )

            # Filter the queryset with the search vector and search rank
            queryset = (
                queryset.annotate(
                    rank=SearchRank(search_vector, partial_search_query),
                    similarity=TrigramSimilarity("title", search_query)
                    + TrigramSimilarity("description", search_query),
                )
                .filter(Q(similarity__gt=0.2) | Q(rank__gte=0.2))
                .order_by("-rank")
            )
        return queryset
