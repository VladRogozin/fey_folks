from django.urls import path

from . import views

app_name = 'random'

urlpatterns = [
    path("random/", views.send_message_to_random_users, name="random"),
    path('list/', views.message_list, name='list'),
    path('messages', views.random_messages_form, name='form')
]