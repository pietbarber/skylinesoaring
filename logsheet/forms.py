
from django import forms
from django.core.exceptions import ValidationError
from .models import Logsheet
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

from .models import Logsheet, Airfield

from django import forms
from django.core.exceptions import ValidationError
from logsheet.models import Logsheet, Towplane, Airfield
from members.models import Member

class CreateLogsheetForm(forms.ModelForm):
    class Meta:
        model = Logsheet
        fields = [
            "log_date", "airfield",
            "duty_officer", "assistant_duty_officer",
            "duty_instructor", "surge_instructor",
            "tow_pilot", "surge_tow_pilot",
            "default_towplane",
        ]
        widgets = {
            "log_date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        log_date = cleaned_data.get("log_date")
        airfield = cleaned_data.get("airfield")

        if log_date and airfield:
            if Logsheet.objects.filter(log_date=log_date, airfield=airfield).exists():
                raise ValidationError("A logsheet for this date and airfield already exists.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["log_date"].widget.attrs.update({"class": "form-control"})
        self.fields["airfield"].queryset = Airfield.objects.filter(is_active=True).order_by("name")
        self.fields["airfield"].widget.attrs.update({"class": "form-select"})

        default_airfield = Airfield.objects.filter(identifier="KFRR").first()
        if default_airfield:
            self.fields["airfield"].initial = default_airfield

        # Setup filtered querysets for each duty crew role
        self.fields["duty_officer"].queryset = Member.objects.filter(duty_officer=True).order_by("last_name")
        self.fields["assistant_duty_officer"].queryset = Member.objects.filter(assistant_duty_officer=True).order_by("last_name")
        self.fields["duty_instructor"].queryset = Member.objects.filter(instructor=True).order_by("last_name")
        self.fields["surge_instructor"].queryset = Member.objects.filter(instructor=True).order_by("last_name")
        self.fields["tow_pilot"].queryset = Member.objects.filter(towpilot=True).order_by("last_name")
        self.fields["surge_tow_pilot"].queryset = Member.objects.filter(towpilot=True).order_by("last_name")
        self.fields["default_towplane"].queryset = Towplane.objects.all().order_by("name", "registration")

        # Optional: set widget styles for dropdowns
        for name in [
            "duty_officer", "assistant_duty_officer",
            "duty_instructor", "surge_instructor",
            "tow_pilot", "surge_tow_pilot",
            "default_towplane",
        ]:
            self.fields[name].required = False
            self.fields[name].widget.attrs.update({"class": "form-select"})