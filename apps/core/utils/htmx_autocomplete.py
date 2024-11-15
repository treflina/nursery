from autocomplete import HTMXAutoComplete
from django.utils.translation import gettext_lazy as _

from apps.kids.models import Child


class ChildHTMXAutocomplete(HTMXAutoComplete):
    """Autocomplete component to select Data Sources from a library"""

    name = "child"
    model = Child
    minimum_search_length = 2
    no_result_text = _("No results found")
    placeholder = _("Start typing child's name")

    def get_items(self, search=None, values=None):
        data = Child.objects.all()
        if search is not None:
            items = [
                {"label": str(x), "value": str(x.id)}
                for x in data
                # Refactor so equality comparison is a function passed in?
                if search == "" or str(search).upper() in f"{x}".upper()
            ]
            return items
        if values is not None:
            items = [
                {"label": str(x), "value": str(x.id)}
                for x in data
                if str(x.id) in values
            ]
            return items

        return []
