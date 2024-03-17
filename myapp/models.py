from django.db import models

# Create your models here.


class Trip(models.Model):
    travel_from = models.CharField(max_length=100)
    travel_to = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    travellers = models.IntegerField()