from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path("", views.index, name="index"),
    path("room/<str:username>/", views.room, name="room"),
    path('chats_list/', views.get_users_with_common_chats, name="chats_list"),
    path('give_permission/<int:chat_id>/', views.give_permission, name='give_permission'),
]