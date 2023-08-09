from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login
from .form import LoginForm
from random_messages.models import RandomPost


def front_view(request):
    posts = RandomPost.objects.all()  # Получение всех объектов модели RandomPost

    return render(request, 'front/front.html', {'posts': posts})

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
