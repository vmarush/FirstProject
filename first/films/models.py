from django.db import models


class Films(models.Model):
    name_film = models.CharField(max_length=50, blank=True)
    producer = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(blank=True)
    rating = models.IntegerField(default=0)
    awards = models.CharField(max_length=50, null=True, blank=True)
    genre = models.ForeignKey("Category", on_delete=models.DO_NOTHING, null=True, blank=True, related_name='films')

    def __str__(self):
        # строковое представление объекта
        return f"Фильм №{self.id} Название: {self.name_film} год: {self.year}"


class Category(models.Model):
    category = models.CharField(max_length=50)

    def __str__(self):
        # строковое представление объекта
        return f"Жанр {self.id} => {self.category} "
