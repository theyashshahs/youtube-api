def paginationTypeByField(PaginationClass, field, page_item_count=5, page_size_param=None):
    class CustomPaginationClass(PaginationClass):
        ordering = field

        def get_page_size(self, request):
            _page_size = page_item_count

            if page_size_param:
                if page_size_param in request.GET:
                    _page_size = request.GET.get(page_size_param)
                    if _page_size.isnumeric():
                        _page_size = int(_page_size)
                    else:
                        _page_size = page_item_count

            return _page_size

    return CustomPaginationClass
