import uuid

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models
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


@login_required
def get_users_with_common_chats(request):
    # Получаем текущего пользователя (предполагается, что аутентификация работает)
    user = request.user

    # Находим все чаты, в которых участвует текущий пользователь как user1 или user2
    common_chats = Chat.objects.filter(models.Q(user1=user) | models.Q(user2=user))

    # Получаем список всех пользователей, участвующих в найденных чатах, кроме текущего пользователя
    users_in_chats = []
    for chat in common_chats:
        if chat.user1 != user:
            users_in_chats.append(chat.user1)
        if chat.user2 != user:
            users_in_chats.append(chat.user2)

    # Используем множество (set) для удаления дубликатов пользователей
    users_with_common_chats = set(users_in_chats)

    # Добавляем информацию о последних сообщениях к каждому пользователю
    for user in users_with_common_chats:
        last_message = Message.objects.filter(chat__user1=user, chat__user2=request.user).order_by('-timestamp').first()
        user.last_message = last_message

    return render(request, 'chat/chats.html', {'users_with_common_chats': users_with_common_chats})


@login_required
def give_permission(request, chat_id):
    # Получаем объект чата или возвращаем 404, если чат не существует
    chat = get_object_or_404(Chat, id=chat_id)

    # Проверяем, является ли текущий пользователь одним из участников чата
    if request.user == chat.user1:
        # Если текущий пользователь - user1, устанавливаем permission_user1 в True
        chat.permission_user1 = True
        chat.save()
    elif request.user == chat.user2:
        # Если текущий пользователь - user2, устанавливаем permission_user2 в True
        chat.permission_user2 = True
        chat.save()

    # Перенаправляем пользователя на страницу с чатами или куда вам нужно
    return redirect('front:front')
