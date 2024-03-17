from django.urls import path, re_path
from myapp import views
from .views import *




urlpatterns = [
    path('', views.home, name='home'),
    path('trippn', views.trippn, name='trippn'),
    path('schedule', views.schedule, name='schedule'),
    path('create-trip/', create_trip, name='create_trip'),
    # path('last_trip_json', last_trip_json, name='last_trip_json'),


    




]