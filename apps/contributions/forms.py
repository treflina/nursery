from django import forms

from .models import Contribution, ContributionStatus


class ContributionStatusForm(forms.ModelForm):

    class Meta:
        fields = ("contribution", "child", "paid", "not_applicable")


class ContributionForm(forms.ModelForm):

    class Meta:
        model = Contribution
        fields = ("name", "name_full", "amount")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        base_class = """border-2 border-blue-300 rounded-md \
            focus:ring-[#92F398] focus:border-[#92F398]"""
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": base_class})
        self.fields["name"].label = "Nazwa krótka"
        self.fields["name_full"].label = "Nazwa pełna dla rodziców"
        self.fields["amount"].label = "Kwota"
