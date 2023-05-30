from django.shortcuts import render
from .models import Book, Genre, Publisher

#модели со связью многие ко многим
#Choices поля
#отобразить все записи в шаблоне
#cоздать отдельный html файл
# создать вьюшку обрабатывающий адрес "get_tags"

# получить все тегов в виде (id,название,книги)

def books(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    publishers = Publisher.objects.all()

    return render(request, "templates/index.html", context={"books": books,
                                                            "genres": genres,
                                                            "publishers": publishers})
