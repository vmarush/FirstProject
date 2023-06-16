from django.shortcuts import render
from django.http import HttpResponse
from .forms import UserForm
def register_user(request):
    form = UserForm()

    return render(request,"register.html",context={"form":form})