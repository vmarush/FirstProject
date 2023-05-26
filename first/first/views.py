from django.http import HttpResponse

def first(request):
    return HttpResponse("<h1>Здесь будут сайт с книгами</h1>")

def second(request):
    return HttpResponse("<h1>мне 27</h1>")

def third(request):
    return HttpResponse("<h1>что угодно</h1>")