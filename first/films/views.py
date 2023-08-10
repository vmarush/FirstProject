from django.shortcuts import render
from django.http import HttpResponse


def films(request):
    return HttpResponse("Тут будут Фильмы")
