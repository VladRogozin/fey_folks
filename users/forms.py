from django import forms
from django.contrib.auth.hashers import make_password  # Import the hashing function
from .models import CustomUser


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(max_length=30, required=True)  # Добавить поле 'first_name' (имя)
    last_name = forms.CharField(max_length=30, required=True)   # Добавить поле 'last_name' (фамилия)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'avatar', 'age', 'city', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.password = self.cleaned_data["password"]
        if self.cleaned_data["avatar"]:
            user.avatar = self.cleaned_data["avatar"]  # Сохранение аватара
        if commit:
            user.save()
        return user
