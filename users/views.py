from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.utils.decorators import method_decorator
from django.views.generic import ListView
from .forms import CustomUserCreationForm, EditProfileForm
from .models import CustomUser
from chat.models import Chat

from random_messages.models import RandomPost


@login_required
def view_profile(request, user_id=None):
    posts = RandomPost.objects.all()
    user = request.user  # Получите текущего пользователя
    chat = None
    is_own_profile = False  # Добавляем переменную для проверки на собственный профиль

    if user.id == user_id:

        viewed_user = get_object_or_404(CustomUser, id=user_id)
        is_own_profile = True
    elif user_id:
        viewed_user = get_object_or_404(CustomUser, id=user_id)
        # Проверяем, существует ли чат между пользователями
        chat = Chat.objects.filter(
            Q(user1=user, user2=viewed_user) | Q(user1=viewed_user, user2=user)
        ).first()
    else:
        viewed_user = user


    context = {
        'user': viewed_user,
        'chat': chat,
        'is_own_profile': is_own_profile,
        'posts': posts,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', user.id)  # Передача аргумента user.id
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'users/edit.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)  # Включите request.FILES для обработки данных файла
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Вместо использования make_password
            user.save()
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('front:front')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('users:login')


