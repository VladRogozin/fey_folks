from random import sample
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import RandomPostForm
from .models import RandomPost

from .models import RandomMessage, RandomTips
from chat.models import Chat


@login_required
def random_messages_form(request):
    tips = RandomTips.objects.all()
    random_tips = sample(list(tips), 4)
    context = {'random_tips': random_tips}
    return render(request, 'random_messages/random_mess.html', context)


@login_required
def send_message_to_random_users(request):
    if request.method == 'POST':
        sender = request.user
        content = request.POST.get('content')

        all_users = get_user_model().objects.all()

        # Исключаем отправителя из списка получателей
        recipients = all_users.exclude(id=sender.id)

        max_recipients = min(100, len(recipients))
        random_recipients = sample(list(recipients), max_recipients)

        # Отправляем сообщение каждому из выбранных случайных пользователей
        for recipient in random_recipients:
            # Проверяем, есть ли между отправителем и получателем чат
            if not Chat.objects.filter(
                (Q(user1=sender, user2=recipient) | Q(user1=recipient, user2=sender))
            ).exists():
                # Если чата нет, то отправляем сообщение
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
            'id': message.id,
            'sender': message.sender.username,
            'recipient': message.recipient.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
        for message in received_messages
    ]

    # Возвращаем JSON данные
    return JsonResponse({'received_messages': messages_json})


@login_required
def delete_message(request, message_id):
    message = get_object_or_404(RandomMessage, id=message_id)

    # Проверяем, что текущий пользователь может удалять это сообщение (например, он является отправителем)
    if message.sender == request.user or message.recipient == request.user:
        message.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def create_random_post(request):
    if request.method == 'POST':
        form = RandomPostForm(request.POST, request.FILES)
        if form.is_valid():
            # Присвоить текущего пользователя автором поста
            random_post = form.save(commit=False)
            random_post.author_id = request.user
            random_post.save()
            return redirect('front:front')  # Перенаправление на список постов
    else:
        form = RandomPostForm()

    context = {'form': form}
    return render(request, 'random_messages/post_form.html', context)


def post_update_view(request, pk):
    post = get_object_or_404(RandomPost, pk=pk)

    if request.method == 'POST':
        form = RandomPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('front:front')
    else:
        form = RandomPostForm(instance=post)

    return render(request, 'random_messages/post_form.html', {'form': form})


class PostDeleteView(DeleteView):
    model = RandomPost
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('random:post_list')  # Используйте ваше имя URL-маршрута

    def delete(self, request, *args, **kwargs):
        response_data = {'message': 'Post deleted successfully'}
        return JsonResponse(response_data)
