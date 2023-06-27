from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"Тэг: {self.title}"


# вторичная запись
class Book(models.Model):
    title = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    year = models.IntegerField()
    raiting = models.IntegerField(default=0, null=True, blank=True)

    publisher = models.OneToOneField("Publisher", on_delete=models.DO_NOTHING, default=None, null=True, blank=True)

    genre = models.ForeignKey("Genre", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='books')
    tags = models.ManyToManyField("Tag", related_name="books",blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    image = models.ImageField(default='123.jpg')

    user = models.ForeignKey(User,on_delete=models.DO_NOTHING, null=True, blank=True,related_name='books')

    def __str__(self):
        # строковое представление объекта
        return f"Книга: {self.id} Название: {self.title} Автор: {self.autor}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


# первичная запись
class Genre(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        # строковое представление объекта
        return f"Жанр {self.id} => {self.title} "


class Publisher(models.Model):
    LANGUAGES = (
        ("ru", "Russian"),
        ("en", "English"),
        ("fr", "French")
    )
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=2, choices=LANGUAGES)

    def __str__(self):
        # строковое представление объекта
        return f"Издание {self.title} => {self.language} "
