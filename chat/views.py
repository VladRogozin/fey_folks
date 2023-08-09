import uuid

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.db import models
from .models import Chat, Message


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
    messages = Message.objects.filter(chat=chat).order_by('-timestamp')# Здесь ограничиваем 10 последними сообщениями

    return render(request, "chat/room.html", {"room_name": chat.chat_name, "messages": messages, "chat": chat})


@login_required
def delete_chat(request, room_name):
    chat = get_object_or_404(Chat, chat_name=room_name)
    if chat and (chat.user1 == request.user or chat.user2 == request.user):
        chat.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    message.delete()
    return JsonResponse({'success': 'Сообщение успешно удалено'})



@login_required
def toggle_permission(request, chat_name):
    chat = get_object_or_404(Chat, chat_name=chat_name)

    if request.user == chat.user1:
        chat.permission_user1 = not chat.permission_user1
        chat.save()
        return JsonResponse({'success': True, 'newPermission': chat.permission_user1})
    elif request.user == chat.user2:
        chat.permission_user2 = not chat.permission_user2
        chat.save()
        return JsonResponse({'success': True, 'newPermission': chat.permission_user2})
    else:
        return JsonResponse({'success': False})



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

    # Преобразуем данные в JSON
    users_data = []
    users_without_messages = []

    for chat in common_chats:
        other_user = chat.user1 if chat.user1 != user else chat.user2
        last_message = chat.last_message
        if last_message:
            user_data = {
                'id': other_user.id,
                'username': other_user.username,
                'avatar_url': other_user.avatar.url if other_user.avatar else None,
                'last_message': last_message.content,
                'last_message_timestamp': last_message.timestamp,
            }
            users_data.append(user_data)
        else:
            users_without_messages.append(other_user)

    users_data = sorted(users_data, key=lambda x: x['last_message_timestamp'], reverse=True)

    # Добавляем пользователей без сообщений в конец списка
    for user in users_without_messages:
        user_data = {
            'id': user.id,
            'username': user.username,
            'avatar_url': user.avatar.url if user.avatar else None,
            'last_message': None,
            'last_message_timestamp': None,
        }
        users_data.append(user_data)

    return JsonResponse({'users_with_common_chats': users_data})



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


@login_required
def upload_chat_background(request, chat_name):
    chat = get_object_or_404(Chat, chat_name=chat_name)

    # Проверяем, что текущий пользователь является user1 или user2 чата
    if request.user == chat.user1:
        background_field = 'background_image_1'
    elif request.user == chat.user2:
        background_field = 'background_image_2'
    else:
        return JsonResponse({'error': 'У вас нет разрешения на изменение фона чата'})

    if request.method == 'POST' and request.FILES.get('background_image'):
        background_image = request.FILES['background_image']

        # Удаляем старое изображение перед сохранением нового
        if getattr(chat, background_field):
            old_background = getattr(chat, background_field)
            old_background.delete()

        # Сохраняем новое изображение в соответствующее поле
        setattr(chat, background_field, background_image)
        chat.save()

        return JsonResponse({'success': 'Изображение фона чата успешно сохранено'})

    return JsonResponse({'error': 'Произошла ошибка при загрузке изображения'})


