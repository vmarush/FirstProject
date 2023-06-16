from django.shortcuts import render, redirect
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
    if request.method == "GET":
        form = BookForm()
        return render(request, "add_book.html", context={"form": form})
    elif request.method == "POST":
        publisher_id = request.POST['publisher']
        genre_id = request.POST['genre']

        image = None

        if publisher_id != '':
            publisher = Publisher.objects.get(id=publisher_id)
        else:
            publisher = None
        if genre_id != '':
            genre = Genre.objects.get(id=genre_id)
        else:
            genre = None

        if request.FILES['image'] != '':
            image = request.FILES['image']



        book = Book.objects.create(title = request.POST['title'],
                            autor = request.POST['autor'],
                            year=request.POST['year'],
                            raiting=request.POST['raiting'],
                            publisher=publisher,
                            genre=genre,
                            image=image)
        tags = request.POST.getlist('tags')
        book.tags.set(tags)
        book.save()

        return redirect("books")



def search_book(request):
    title = request.GET['title']
    genre = request.GET['genre']

    books = Book.objects.all()

    if title != '':
        books = books.filter(title__contains=title)

    if genre != '':
        books = books.filter(genre__title__contains=genre)

    return render(request, 'search_book.html', context={"books": books})


def delete_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>книги с таким айди {id} не существует</h1>")

    book.delete()

    return redirect('books')
