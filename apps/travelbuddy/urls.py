from django.conf.urls import url,include
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^travels$', views.travels),
    url(r'^travels/add$', views.addTrip),
    url(r'^travels/process$', views.tripProcess),
    url(r'^travels/destination/(?P<id>\d+)$', views.tripDetail),
    url(r'^travels/join/(?P<trip_id>\d+)/(?P<user_id>\d+)$', views.tripJoin),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^logout$', views.logout),
]
