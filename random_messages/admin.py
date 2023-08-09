from django.contrib import admin
from .models import RandomTips


class RandomTipsAdmin(admin.ModelAdmin):
    list_display = ('chat_name', 'text')  # Отображаемые поля в списке записей
    search_fields = ('chat_name', 'text')  # Поля для поиска
    list_filter = ('chat_name',)  # Фильтры


admin.site.register(RandomTips, RandomTipsAdmin)
