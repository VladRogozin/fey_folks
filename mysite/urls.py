from django.contrib import admin
from django.urls import include, path

from front.views import front_view


urlpatterns = [
    path('', front_view, name='front'),
    path("chat/", include("chat.urls")),
    path("admin/", admin.site.urls),
    path('users/', include("users.urls")),

]

