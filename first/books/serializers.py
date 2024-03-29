from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Book, Genre, Publisher, Tag, Comment
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError


class CreateBookSerializer(ModelSerializer):
    tags = serializers.CharField(required=False)
    user = serializers.CharField(required=False)
    genre = serializers.CharField(required=False)

    def validate_tags(self, value: str):
        list_of_ids = value.split(', ')
        tags = []
        try:
            for tag_id in list_of_ids:
                tag = Tag.objects.get(id=tag_id)
                tags.append(tag)
        except Tag.DoesNotExist:
            raise ValidationError('таких тегов не найдено')
        return tags

    def validate_user(self, value: str):
        try:
            user = User.objects.get(username=value)
        except User.DoesNotExist:
            raise ValidationError('пользователя с таким именем не найдено')

        return user

    def validate_genre(self, value: str):
        try:
            genre = Genre.objects.get(title=value)
        except Genre.DoesNotExist:
            raise ValidationError('жанра с таким названием не найдено')

        return genre

    class Meta:
        model = Book
        fields = ['title', 'autor', 'year', 'raiting', 'price', 'genre', 'tags', 'user']


class GenreBookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'autor', 'price', 'count']


class GenreSerializer(ModelSerializer):
    books = GenreBookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'title', 'books']


class GenreSerializerTest(ModelSerializer):
    # books = GenreBookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'title']


class PublisherBookSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id', 'title', 'language']


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']


class BookSerializer(ModelSerializer):
    genre_title = serializers.SerializerMethodField()
    publisher_title = serializers.SerializerMethodField()

    tag1 = serializers.SerializerMethodField()

    def get_tag1(self, obj):
        list1 = []
        for i in obj.tags.all():
            list1.append(i.title)

        return list1

    def get_genre_title(self, obj):
        try:
            return obj.genre.title
        except AttributeError:
            return 'нет жанра'

    def get_publisher_title(self, obj):
        if obj.publisher is not None:
            return obj.publisher.title
        return 'нет жанра'

    class Meta:
        model = Book
        fields = ['id', 'title', 'autor', 'genre_title', 'publisher_title', 'tag1', 'year']
