from django.shortcuts import render
from .models import Book, Genre, Publisher, Tag
from django.http import HttpResponse
from .forms import BookForm


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


def get_genre_books(request, title):
    try:
        genre = Genre.objects.get(title=title)
    except Genre.DoesNotExist:
        return HttpResponse(f"<h1>жанра с таким названием {title} не существует</h1>")
    return render(request, "templates/genre.html", context={"genre": genre})


def get_tag_books(request, title):
    try:
        tag = Tag.objects.get(title=title)
    except Tag.DoesNotExist:
        return HttpResponse(f"<h1>Тега с таким названием {title} не существует</h1>")
    tag_books = tag.books.all()
    return render(request, "templates/tag_detail.html", context={"tag_books": tag_books,
                                                                 "tag": tag})


def add_book(request):
    form = BookForm()
    return render(request, "templates/add_book.html", context={'form':form})


def create_book(request):
    print(request.POST)
    genre = Genre.objects.get(id=request.Post['genre'])
    print(genre)
    Book.objects.create(title=request.Post['title'],
                        autor=request.Post['autor'],
                        tags=request.Post['tags'],
                        raiting=request.Post['raiting'],
                        # publisher=request.Post['publisher'],
                        genre=genre
                        )
    return HttpResponse("<h1>получилось!</h1>")
