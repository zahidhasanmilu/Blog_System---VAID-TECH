from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    # প্রতি পেজে কতগুলো আইটেম থাকবে
    page_size = 3
    page_size_query_param = (
        "page_size"  # চাইলে URL থেকে override করা যাবে (?page_size=10)
    )
    max_page_size = 50

    def get_paginated_response(self, data):
        # যদি কোন রেজাল্ট না থাকে
        if not data:
            return Response({"message": "No results found.", "results": []})

        # অন্যথায় normal pagination response
        return Response(
            {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "current_page": self.page.number,
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,
            }
        )
