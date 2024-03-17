from django.contrib import admin

# Register your models here.

from .models import Trip

# Define an admin class if you want to customize the admin interface for the model
class TripAdmin(admin.ModelAdmin):
    # Customize how the model is displayed in the admin interface, e.g., list_display, search_fields, etc.
    list_display = ('travel_from', 'travel_to', 'start_date', 'end_date', 'travellers')

# Register the model along with its admin class
admin.site.register(Trip, TripAdmin)