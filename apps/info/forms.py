from datetime import timedelta

from django import forms

from .models import Activities, MainTopic


class ActivitiesInfoForm(forms.ModelForm):

    class Meta:
        model = Activities
        fields = (
            "day",
            "topic",
            "activity",
            "movement",
            "music",
            "art",
            "other",
            "special_event",
        )

        widgets = {"day": forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        last_activity = Activities.objects.all().order_by("day").last()
        if last_activity:
            self.fields["day"].initial = last_activity.day + timedelta(days=1)

        base_class = """border-2 border-blue-300 rounded-md \
            focus:ring-[#92F398] focus:border-[#92F398]"""
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": base_class})
        for field in ["activity", "movement", "music", "art", "other", "special_event"]:
            self.fields[field].widget.attrs.update({"rows": "3"})


class MainTopicForm(forms.ModelForm):

    class Meta:
        model = MainTopic
        fields = ("description",)
