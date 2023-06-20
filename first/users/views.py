from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm
from django.contrib.auth.models import User


def register_user(request):
    if request.method == "GET":
        form = UserForm()

        return render(request, "register.html", context={"form": form})
    else:
        user = User.objects.create_user(username=request.POST['username'],
                                        email=request.POST['email'])

        user.set_password(request.POST['password'])
        user.save()
        return redirect('books')
