from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, LoginUserForm
from django.contrib.auth.models import User
import django
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


def register_user(request):
    if request.method == "GET":
        form = UserForm()

        return render(request, "register.html", context={"form": form})
    else:
        email = request.POST['email']
        if User.objects.filter(email=email).count() != 0:
            return HttpResponse("<h1>Такой email уже используется</h1>")
        else:
            try:
                user = User.objects.create_user(username=request.POST['username'],
                                                email=email)
            except django.db.utils.IntegrityError:

                return HttpResponse("<h1>Такой пользователь уже используется</h1>")

            user.set_password(request.POST['password'])
            user.save()

            send_mail("Успешня регистрация", "вы успешно зарегестрирывались", settings.DEFAULT_FROM_EMAIL, settings.RECIPIENTS_EMAIL)

            return HttpResponse("<h1>вы успешно зарегистрировались</h1>")


def login_user(request):
    if request.method == "GET":
        form = LoginUserForm()

        return render(request, "login_user.html", context={"form": form})
    else:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user=user)
        else:
            return HttpResponse("<h1>неверные данные</h1>")

        return redirect('books')


def logout_user(request):

    if request.user.is_authenticated:
        logout(request)
        if request.environ['HTTP_REFERER'] == 'http://127.0.0.1:8000/get_books/':
            return redirect('books')
        elif request.environ['HTTP_REFERER'] == 'http://127.0.0.1:8000/posts/':
            return redirect('posts')
    else:
        return HttpResponse("<h1>404</h1>")
