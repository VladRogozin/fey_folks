import random

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect

from .models import RandomMessage


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

        return redirect('front:front')

    return render(request, 'sss')


def message_list(request):
    user = request.user
    received_messages = RandomMessage.objects.filter(recipient=user)
    return render(request, 'random_messages/rand_mess_list.html', {'received_messages': received_messages})