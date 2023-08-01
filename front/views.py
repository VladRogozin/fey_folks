from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth import get_user_model

from chat.models import Chat


def front_view(request):
    users = get_user_model().objects.all()
    chats = Chat.objects.none()  # Initialize an empty queryset
    current_user = request.user  # Get the current user

    if current_user.is_authenticated:
        chats = Chat.objects.filter(Q(user1=current_user) | Q(user2=current_user))

    return render(request, 'front/front.html', {'users': users, 'chats': chats, 'current_user': current_user})
