import random
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json
from .models import RandomMessage


@login_required
def random_messages_form(request):
    return render(request, 'random_messages/random_mess.html')


@login_required
def send_message_to_random_users(request):
    if request.method == 'POST':
        sender = request.user  # Получаем текущего пользователя (предполагается, что аутентификация работает)
        content = request.POST.get('content')  # Получаем содержимое сообщения из формы

        # Получаем всех пользователей из базы данных
        all_users = get_user_model().objects.all()

        # Исключаем отправителя из списка получателей
        recipients = all_users.exclude(id=sender.id)

        # Выбираем 5 случайных пользователей из получателей
        random_recipients = random.sample(list(recipients), 3)

        # Отправляем сообщение каждому из выбранных случайных пользователей
        for recipient in random_recipients:
            message = RandomMessage.objects.create(sender=sender, recipient=recipient, content=content)

        return redirect('random:form')

    return render(request, 'sss')


@login_required
def message_list(request):
    user = request.user
    received_messages = RandomMessage.objects.filter(recipient=user)

    # Сериализуем сообщения в формат JSON
    messages_json = [
        {
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in received_messages
    ]

    # Возвращаем JSON данные
    return JsonResponse({'received_messages': messages_json})