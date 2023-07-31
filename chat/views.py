import uuid

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .models import Chat, Message


@login_required
def index(request):
    users = get_user_model().objects.exclude(pk=request.user.pk)  # Исключаем текущего пользователя из списка
    return render(request, "chat/index.html", {"users": users})

@login_required
def room(request, username):
    user1 = request.user
    user2 = get_object_or_404(get_user_model(), username=username)

    # Проверяем, существует ли чат между пользователями (user1=user1, user2=user2)
    chat = Chat.objects.filter(user1=user1, user2=user2).first()

    # Если чат не был найден, ищем чат с (user1=user2, user2=user1)
    if not chat:
        chat = Chat.objects.filter(user1=user2, user2=user1).first()

    # Если чат не был найден, создаем новый чат
    if not chat:
        chat = Chat.objects.create(user1=user1, user2=user2)
        # Если чат был создан только что, то генерируем уникальное имя чата
        user_1 = user1.username.lower()
        user_2 = user2.username.lower()
        chat.chat_name = str(user_2 + user_1)  # Генерируем случайное имя
        chat.save()

    # Проверяем, является ли текущий пользователь одним из участников чата
    if request.user not in [chat.user1, chat.user2]:
        return redirect('some_other_page')  # или отобразите сообщение об ошибке

    # Получаем последние сообщения из чата
    messages = Message.objects.filter(chat=chat).order_by('-timestamp')[:10]# Здесь ограничиваем 10 последними сообщениями

    return render(request, "chat/room.html", {"room_name": chat.chat_name, "messages": messages})
