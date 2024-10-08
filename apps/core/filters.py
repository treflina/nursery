import operator
from functools import reduce

import django_filters
from django.db.models import Q
from django.forms import TextInput


# Custom widget that uses search input type
class SearchInput(TextInput):
    input_type = "search"


class BaseFilter(django_filters.FilterSet):

    query = django_filters.CharFilter(
        method="child_search",
        label="",
        widget=SearchInput(attrs={"placeholder": "Search..."}),
    )

    def child_search(self, queryset, name, value):
        query_words = value.split()

        return queryset.filter(
            reduce(
                operator.and_,
                (
                    Q(child__first_name__icontains=word)
                    | Q(child__last_name__icontains=word)
                    for word in query_words
                ),
            )
        )
