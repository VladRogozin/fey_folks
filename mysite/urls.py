from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', include('front.urls', namespace='front')),
    path("chat/", include("chat.urls", namespace='chat')),
    path("admin/", admin.site.urls),
    path('users/', include("users.urls")),
    path('random/', include("random_messages.urls"))

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)