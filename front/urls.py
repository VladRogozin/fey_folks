from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('', views.front_view, name='front'),
    path('hello', views.unauthorized, name='hello'),
]