# app_drf/filters.py
import django_filters
from blog.models import Blog


# BaseInFilter কে subclass করে বানাতে হবে
class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class BlogFilter(django_filters.FilterSet):
    # title contains
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")

    # একাধিক category title দিয়ে filter (comma separated)
    category = CharInFilter(field_name="category__title", lookup_expr="in")

    # একাধিক tag title দিয়ে filter (comma separated)
    tags = CharInFilter(field_name="tags__title", lookup_expr="in")

    class Meta:
        model = Blog
        fields = ["title", "category", "tags"]
