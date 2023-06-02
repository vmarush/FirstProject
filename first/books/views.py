from django.shortcuts import render
from .models import Book, Genre, Publisher
from django.http import HttpResponse


def books(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    publishers = Publisher.objects.all()

    return render(request, "templates/index.html", context={"books": books,
                                                            "genres": genres,
                                                            "publishers": publishers})


def get_book(request, id):

    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>книги с таким айди {id} не существует</h1>")

    # return HttpResponse(f"<h1>Детальная инфа о книге {book.title}</h1>")
    return render(request, "templates/detali.html", context={"book": book})

def get_genre_books(request,title):
    try:
        genre = Genre.objects.get(title=title)
    except Genre.DoesNotExist:
        return HttpResponse(f"<h1>жанра с таким названием {title} не существует</h1>")
    return render(request, "templates/genre.html", context={"genre": genre})
