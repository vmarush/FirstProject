import requests
from django.db.migrations import serializer
from django.shortcuts import render, redirect
from .models import Book, Genre, Publisher, Tag, Comment, Favorite
from django.http import HttpResponse
from .forms import BookForm
import django
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import JsonResponse
from .serializers import BookSerializer, GenreSerializer, CreateBookSerializer, GenreSerializerTest, \
    PublisherBookSerializer,CommentSerializer
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action

def get_all_comments(request):
    coments = Comment.objects.all()
    serializer = CommentSerializer(coments,many=True)
    return JsonResponse(data=serializer)

class BookViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=True,methods=['GET'])
    def comments(self,request,pk=None):
        book = self.get_object()

        comments = book.comments.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(data=serializer.data)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        serializer = serializer(data=request.POST)
        if not serializer.is_valid():
            return Response(data=serializer.errors)
        tags = None
        book = Book.objects.create(**serializer.validated_data)
        if serializer.validated_data.get('tags'):
            tags = serializer.validated_data.get('tags')
        if tags:
            book.tags.set(tags)
            book.save()
        BookSerializer(book)
        return Response(data=BookSerializer(book).data)

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateBookSerializer
        return BookSerializer


def get_all_publishers(request):
    publishers = Publisher.objects.all()
    serializer = PublisherBookSerializer(publishers, many=True)
    return JsonResponse(data=serializer.data, safe=False)


def get_all_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return JsonResponse(data=serializer.data, safe=False)


def get_all_genre(request):
    genres = Genre.objects.all()
    serializer = GenreSerializerTest(genres, many=True)
    return JsonResponse(data=serializer.data, safe=False)


def book_detail(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse(data={'id': 'Book not found'})
    serializer_data = BookSerializer(book)

    return JsonResponse(data=serializer_data.data)


@api_view(['POST', ])
def create_book(request):
    serializer = CreateBookSerializer(data=request.POST)

    if serializer.is_valid():
        print('все данные валидны')
    else:
        print(serializer.errors)
        return JsonResponse(data=serializer.errors)
    tags = serializer.validated_data.pop('tags')
    book = Book.objects.create(**serializer.validated_data)
    book.tags.set(tags)
    book.save()

    serializer = BookSerializer(book)
    return JsonResponse(data=serializer.data)


@api_view(['PATCH', ])
def update_book_api(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse(data={'id': 'Book not found'})
    serializer = CreateBookSerializer(data=request.POST)
    if serializer.is_valid():
        print('все данные валидны')
    else:
        print(serializer.errors)
        return JsonResponse(data=serializer.errors)
    book.title = serializer.validated_data['title']
    book.autor = serializer.validated_data['autor']
    book.price = serializer.validated_data['price']
    book.year = serializer.validated_data['year']
    book.user = serializer.validated_data.get('user', book.user)

    if 'tags' in serializer.validated_data.keys():
        book.tags.set(serializer.validated_data['tags'])

    book.save()
    return JsonResponse(data={'vadim': 'vadim'})


@api_view(['DELETE', ])
def delete_book_api(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return JsonResponse(data={'messege': 'Такой книги не существует'})
    book.delete()
    return JsonResponse(data={'message': 'книга удалена'})


class BookListView(ListView):
    model = Book
    context_object_name = 'my_new_books'
    queryset = Book.objects.all()

    def get_context_data(self, **kwargs):
        # получение первичного контента
        context = super().get_context_data(**kwargs)
        # запрос в бд для получения всех тегов
        tags = Tag.objects.all()
        context['tags'] = tags
        return context


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.get_object()
        show_favorite_button = True

        if self.request.user.is_authenticated:
            if Favorite.objects.filter(book=book, user=self.request.user):
                show_favorite_button = False

        context['show_favorite_button'] = show_favorite_button
        return context


# def books(request):
#     books = Book.objects.all()
#     genres = Genre.objects.all()
#     publishers = Publisher.objects.all()
#
#     return render(request, "templates/index.html", context={"books": books,
#                                                             "genres": genres,
#                                                             "publishers": publishers})


# def get_book(request, id):
#     try:
#         book = Book.objects.get(id=id)
#     except Book.DoesNotExist:
#         return HttpResponse(f"<h1>книги с таким айди {id} не существует</h1>")
#
#     show_favorite_button = True
#     if request.user.is_authenticated:
#         if Favorite.objects.filter(book=book,user=request.user):
#             show_favorite_button = False
#     return render(request, "templates/detali.html", context={"book": book,
#                                                              'show_favorite_button':show_favorite_button})


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
                                       user=request.user,
                                       price=request.POST['price'])
            tags = request.POST.getlist('tags')
            book.tags.set(tags)
            book.save()

            return redirect("books")
    else:
        return HttpResponse(f"<h1>у вас нет прав</h1>")


def search_book_by_tags(request):
    tags_input: str = request.GET['tags_input']
    messeges = []
    tags_list = tags_input.split(', ')
    tags = []
    tag_books = []
    for tag_title in tags_list:
        try:
            tag = Tag.objects.get(title=tag_title)
            tags.append(tag)
        except Tag.DoesNotExist:
            messeges.append(f'Туга с таким названием не существует!: {tag_title} ')

    for tag in tags:
        for book in tag.books.all():
            tag_books.append(book)

    return render(request, "templates/tag_detail.html", context={"tag_books": set(tag_books),
                                                                 "tag": None,
                                                                 'messeges': messeges})


def search_book(request):
    title = request.GET['title']
    genre = request.GET['genre']
    price_lt = request.GET['price_lt']

    books = Book.objects.all()
    result_string = "Результат поиска"

    if title != '':
        result_string += f"по названию {title} "
        books = books.filter(title__contains=title)

    if genre != '':
        result_string += f"по жанру {genre} "
        books = books.filter(genre__title__contains=genre)

    if price_lt != '':
        result_string += f"по цене {price_lt} "
        books = books.filter(price__lte=price_lt)

    return render(request, 'search_book.html', context={"books": books,
                                                        "result_string": result_string})


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
            return redirect('get_book', pk=book.id)


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
        return redirect('get_book', pk=id)
    else:
        return HttpResponse(f"<h1>введите коректный адресс </h1>")


def buy_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse(f"<h1>такой книги нет </h1>")

    if book.count != 0:
        book.count = book.count - 1
        book.save()
    else:
        return HttpResponse(f"<h1> 404 </h1>")

    return HttpResponse(f"<h1>buy book </h1>")


def favorite_book(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse('<h1>404</h1>')
    if not request.user.is_authenticated:
        return HttpResponse('<h1>404</h1>')

    Favorite.objects.create(book=book,
                            user=request.user)
    return redirect('get_book', pk=book.id)


def favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user)
        return render(request, 'favorites.html', context={"favorites": favorites
                                                          })
    else:
        return HttpResponse('<h1>404</h1>')


def delete_from_favorites(request, id):
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return HttpResponse('<h1>404</h1>')
    if request.user.is_authenticated:
        favorite = Favorite.objects.get(user=request.user, book=book)

        favorite.delete()

        return redirect('favorites')
    return HttpResponse('<h1>404</h1>')
