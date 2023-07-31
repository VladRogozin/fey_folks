from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("room/<str:username>/", views.room, name="room"),
]