from django.urls import path

from . import views

app_name = 'chat'

urlpatterns = [
    path("room/<str:username>/", views.room, name="room"),
    path('chats_list/', views.get_users_with_common_chats, name="chats_list"),
    path('give_permission/<int:chat_id>/', views.give_permission, name='give_permission'),
    path("delete_chat/<str:room_name>/", views.delete_chat, name="delete_chat"),
]