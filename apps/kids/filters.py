import operator
from functools import reduce

from django.db.models import Q

from apps.core.filters import BaseFilter

from .models import Child


class ChildFilter(BaseFilter):

    def child_search(self, queryset, name, value):
        query_words = value.split()

        return queryset.filter(
            reduce(
                operator.and_,
                (
                    Q(first_name__icontains=word) | Q(last_name__icontains=word)
                    for word in query_words
                ),
            )
        )

    class Meta:
        model = Child
        fields = ["query"]
