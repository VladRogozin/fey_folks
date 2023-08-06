from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/<int:user_id>', views.view_profile, name='profile'),
    path('edit/', views.edit_profile, name='edit'),
]