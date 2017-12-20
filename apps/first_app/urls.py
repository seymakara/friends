from django.conf.urls import url
from . import views           
urlpatterns = [
    url(r'^main$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^friends$', views.show_friends),
    url(r'^users/add/(?P<id>\d+)$', views.add_friend),
    url(r'^users/remove/(?P<id>\d+)$', views.remove_friend),
    url(r'^users/(?P<id>\d+)$', views.show_profile),
    url(r'^$', views.index),
]