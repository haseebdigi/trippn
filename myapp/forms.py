# forms.py
from django import forms
from .models import Trip

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ['travel_from', 'travel_to', 'start_date', 'end_date', 'travellers']
