from django.shortcuts import render
from django.contrib.auth import get_user_model


def front_view(request):
    users = get_user_model().objects.all()
    return render(request, 'front/front.html', {'users': users})
