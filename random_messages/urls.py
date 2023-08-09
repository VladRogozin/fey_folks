from django.urls import path

from . import views

from .views import (

    PostDeleteView,
)


app_name = 'random'

urlpatterns = [
    path("random/", views.send_message_to_random_users, name="random"),
    path('list/', views.message_list, name='list'),
    path('messages/', views.random_messages_form, name='form'),
    path("delete_message/<int:message_id>/", views.delete_message, name="delete_message"),
    path('random/post/create/', views.create_random_post, name='create-random-post'),
    path('post/update/<int:pk>/', views.post_update_view, name='post-update'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
]