from django.shortcuts import render, redirect
from .models import Book, Genre, Publisher, Tag, Comment
from django.http import HttpResponse
from .forms import BookForm
import django

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
    if request.user.is_authenticated:
        if request.method == "GET":
            form = BookForm()
            return render(request, "add_book.html", context={"form": form})
        elif request.method == "POST":
            publisher_id = request.POST['publisher']
            genre_id = request.POST['genre']

            if publisher_id != '':
                publisher = Publisher.objects.get(id=publisher_id)
            else:
                publisher = None
            if genre_id != '':
                genre = Genre.objects.get(id=genre_id)
            else:
                genre = None

            image = request.FILES.get('image', '123.jpg')

            book = Book.objects.create(title=request.POST['title'],
                                       autor=request.POST['autor'],
                                       year=request.POST['year'],
                                       raiting=request.POST['raiting'],
                                       publisher=publisher,
                                       genre=genre,
                                       image=image,
                                       user=request.user)
            tags = request.POST.getlist('tags')
            book.tags.set(tags)
            book.save()

            return redirect("books")
    else:
        return HttpResponse(f"<h1>у вас нет прав</h1>")


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

    if request.user.username != book.user.username:
        return HttpResponse(f"<h1>у вас нет прав</h1>")
    else:

        book.delete()

        return redirect('books')


def update_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>книги с таким айди {id} не существует</h1>")

    if request.user.username != book.user.username:
        return HttpResponse(f"<h1>у вас нет прав</h1>")
    else:

        if request.method == "GET":
            form = BookForm(instance=book)
            return render(request, 'update_book.html', context={"form": form,
                                                                'book': book})
        else:

            publisher_id = request.POST['publisher']
            genre_id = request.POST['genre']
            image = request.FILES.get('image', "123.jpg")

            if publisher_id != '':
                publisher = Publisher.objects.get(id=publisher_id)
            else:
                publisher = None
            if genre_id != '':
                genre = Genre.objects.get(id=genre_id)
            else:
                genre = None

            book.title = request.POST['title']
            book.autor = request.POST['autor']
            book.year = request.POST['year']
            book.publisher = publisher
            book.raiting = request.POST['raiting']
            book.genre = genre
            book.image = image
            tags = request.POST.getlist('tags')
            book.tags.set(tags)
            book.save()
            return redirect('get_book', id=book.id)


# def add_comment(request, id):
#     print(request.POST)
#     try:
#         raiting = 5
#         book = Book.objects.get(id=id)
#         Comment.objects.create(content=request.POST['comment'],
#                                raiting=raiting,
#                                user=request.user,
#                                book=book)
#         return redirect('get_book', id=id)
#     except django.utils.datastructures.MultiValueDictKeyError:
#         return HttpResponse(f"<h1>вы не добаляете комент </h1>")
#     except Exception:
#         return HttpResponse(f"<h1>введите коректный адресс </h1>")


def add_comment(request, id):
    if request.user.is_authenticated:
        raiting = 5
        try:
            book = Book.objects.get(id=id)
        except Book.DoesNotExist:
            return HttpResponse(f"<h1>нет такоой книги </h1>")
        try:
            Comment.objects.create(content=request.POST['comment'],
                                   raiting=raiting,
                                   user=request.user,
                                   book=book)
        except django.utils.datastructures.MultiValueDictKeyError:
            return HttpResponse(f"<h1>404 </h1>")
        return redirect('get_book', id=id)
    else:
        return HttpResponse(f"<h1>введите коректный адресс </h1>")
