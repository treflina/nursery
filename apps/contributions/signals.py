from django.dispatch import Signal


def create_new_contributionstatus_if_new_contribution(sender, **kwargs):
    if kwargs.get("created", False):
        from apps.kids.models import Child

        from .models import ContributionStatus

        children = Child.objects.all()
        for child in children:
            ContributionStatus.objects.get_or_create(
                child=child, contribution=kwargs.get("instance")
            )
    return kwargs
