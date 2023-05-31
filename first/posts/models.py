from django.db import models


class PostTag(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return f"Тэг: {self.title}"


class Post(models.Model):
    title = models.CharField(max_length=50, blank=True)
    tags = models.ManyToManyField('PostTag', related_name='posts')
    category = models.OneToOneField("Category", on_delete=models.CASCADE, related_name="posts")
    description = models.TextField(blank=True)
    date_create = models.DateTimeField()

    def __str__(self):
        return f"Пост: {self.id} Название: {self.title}"


class Category(models.Model):
    Sense = (
        ("sl", "Stars"),
        ("ds", "Disasters"),
        ("ns", "News"),
        ("pb", "Public"),
        ("h", "Humir")

    )
    title = models.CharField(max_length=50)
    sense = models.CharField(max_length=2, choices=Sense, default="pb")

    def __str__(self):
        return f"Категория {self.title} -> {self.sense} "
