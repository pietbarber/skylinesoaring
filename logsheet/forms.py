
from django import forms
from django.core.exceptions import ValidationError
from .models import Logsheet

class CreateLogsheetForm(forms.ModelForm):
    class Meta:
        model = Logsheet
        fields = ["log_date", "airfield"]
        widgets = {
            "log_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "airfield": forms.TextInput(attrs={"class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        log_date = cleaned_data.get("log_date")
        airfield = cleaned_data.get("airfield")

        if log_date and airfield:
            if Logsheet.objects.filter(log_date=log_date, airfield=airfield).exists():
                raise ValidationError("A logsheet for this date and airfield already exists.")

        return cleaned_data

from django import forms
from .models import Flight
from .models import Towplane
from members.models import Member


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            "launch_time",
            "landing_time",
            "pilot",
            "instructor",
            "glider",
            "towplane",
            "tow_pilot",
            "release_altitude",
        ]
        widgets = {
            "launch_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "landing_time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "pilot": forms.Select(attrs={"class": "form-select"}),
            "instructor": forms.Select(attrs={"class": "form-select"}),
            "glider": forms.Select(attrs={"class": "form-select"}),
            "tow_pilot": forms.Select(attrs={"class": "form-select"}),
            "towplane": forms.Select(attrs={"class": "form-select"}),
            "release_altitude": forms.Select(attrs={"class": "form-select"}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["towplane"].queryset = Towplane.objects.filter(is_active=True)
        # Filter instructors only
        self.fields["instructor"].queryset = Member.objects.filter(instructor=True)
        self.fields["tow_pilot"].queryset = Member.objects.filter(towpilot=True)


