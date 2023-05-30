from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"Тэг: {self.title}"


# вторичная запись
class Book(models.Model):
    title = models.CharField(max_length=50, blank=True)
    autor = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(blank=True)
    raiting = models.IntegerField(default=0)

    publisher = models.OneToOneField("Publisher", on_delete=models.DO_NOTHING, default=None)

    genre = models.ForeignKey("Genre", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='books')
    tags = models.ManyToManyField("Tag", related_name="books")

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
    language = models.CharField(max_length=2, choices=LANGUAGES, default="ru")

    def __str__(self):
        # строковое представление объекта
        return f"Издание {self.title} => {self.language} "
