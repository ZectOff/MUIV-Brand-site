from django.contrib.auth.decorators import login_required
from django.contrib import auth, messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from carts.models import Cart

from users.forms import ProfileForm, ProfileImageForm, UserLoginForm, UserRegistrationForm


def login(request):

    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth.login(request, user)
                messages.success(request, f"{username}, Вы вошли в аккаунт.")

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                redirect_page = request.POST.get('next', None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))
                
                return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserLoginForm()

    context = {
        'title': 'MUIV Brand - Авторизация',
        'form': form,
    }
    return render(request, 'users/login.html', context)

def registration(request):

    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()

            session_key = request.session.session_key

            user = form.instance
            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)
            messages.success(request, f"{user.username}, Вы успешно зарегистрировались и вошли в аккаунт.")
            return HttpResponseRedirect(reverse('main:home'))
    else:
        form = UserRegistrationForm()

    context = {
        'title': 'MUIV Brand - Регистрация',
        'form': form,
    }
    return render(request, 'users/registration.html', context)

@login_required
def profile(request):

    # Код по типу "Активность в сообществе"

    if request.method == "POST":
        form_img = ProfileImageForm(data=request.POST, instance=request.user, files=request.FILES)
        if form_img.is_valid():
            form_img.save()
            messages.success(request, "Аватар успешно обновлен!")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form_img = ProfileForm(instance=request.user)

    context = {
        'title': 'MUIV Brand - Личный кабинет',
        'form_img': form_img,
    }
    return render(request, 'users/profile.html', context)

@login_required
def profile_menu(request, profile_slug=None):

    if request.method == "POST":
        form = ProfileForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные аккаунта успешно обновлены!")
            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)

    context = {
        'title': 'MUIV Brand - Личный кабинет',
        'form': form,
        'url_slug': profile_slug,
    }

    return render(request, 'users/profmenu.html', context)

def users_cart(request):
    context = {
        'title': 'MUIV Brand - Корзина товаров',
    }
    return render(request, 'users/users_cart.html', context)

@login_required
def logout(request):
    messages.warning(request, f"{request.user.username}, Вы вышли из аккаунта")
    auth.logout(request)
    return redirect(reverse('main:home'))