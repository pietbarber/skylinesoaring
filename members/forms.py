from django import forms
from datetime import date, timedelta
from .models import Member
from tinymce.widgets import TinyMCE

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = [
          'id',
          'last_login',
          'is_superuser',
          'username', 'first_name', 'last_name', 'email',
          'is_staff',
          'is_active',
          'SSA_member_number', 'phone', 'mobile_phone',
          'address',
          'city',
          'state',
          'zip_code',
          'profile_photo',
          'glider_rating', 'instructor', 'duty_officer', 'assistant_duty_officer', 'secretary',
          'treasurer', 'webmaster', 'director', 'member_manager',
          'glider_owned',
          'second_glider_owned',
          'joined_club',
          'emergency_contact',
          'public_notes',
          'private_notes',
          'last_updated_by'
        ]

        widgets = {
            'address': forms.Textarea(attrs={'rows': 2}),
            'emergency_contact': forms.Textarea(attrs={'rows': 2}),
            'public_notes': TinyMCE(attrs={'rows': 10}),
            'private_notes': TinyMCE(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["joined_club"].widget = forms.TextInput(
            attrs={
                "class": "form-control datepicker",  # let flatpickr hook onto it
                "placeholder": "YYYY-MM-DD",
                "autocomplete": "off",               # optional: prevents weird autofill
            }
        )
        self.fields["joined_club"].input_formats = ["%Y-%m-%d"]


        # Remove default verbose help text for system fields
        for field in ['username', 'email', 'first_name', 'last_name']:
            self.fields[field].help_text = None

        self.fields['profile_photo'].help_text = "Upload a clear, smiling portrait. 😄"
        self.fields['public_notes'].help_text = "Visible to all members."
        self.fields['private_notes'].help_text = "Visible only to club officers."
