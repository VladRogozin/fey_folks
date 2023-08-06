from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login

from chat.models import Chat

from .form import LoginForm


def front_view(request):
    users = get_user_model().objects.all()
    chats = Chat.objects.none()  # Initialize an empty queryset
    current_user = request.user  # Get the current user

    if current_user.is_authenticated:
        chats = Chat.objects.filter(Q(user1=current_user) | Q(user2=current_user))

    return render(request, 'front/front.html', {'users': users, 'chats': chats, 'current_user': current_user})


def unauthorized(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('front:front')
    else:
        form = LoginForm()

    return render(request, 'front/unauthorized.html', {'form': form})
