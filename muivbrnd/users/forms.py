from dataclasses import field
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ['username', 'password']

    username = forms.CharField() # for example
    password = forms.CharField()

    # username = forms.CharField(
    #     label='Имя пользователя',
    #     widget=forms.TextInput(attrs={'autofocus': True,
    #                                   'class': 'auth-inp',
    #                                   'placeholder': 'Введите имя пользователя'}))
    # password = forms.CharField(
    #     label='Пароль',
    #     widget=forms.PasswordInput(attrs={'autofocus': True,
    #                                       'class': 'auth-inp',
    #                                       'placeholder': 'Введите имя пользователя'}))

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2',
        )

    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()