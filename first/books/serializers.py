from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Book, Genre


class GenreBookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'autor', 'price', 'count']


class GenreSerializer(ModelSerializer):
    # books_titles = serializers.StringRelatedField(many=True, source='books')
    books = GenreBookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'title', 'books']


class BookSerializer(ModelSerializer):
    genre_title = serializers.SerializerMethodField()
    pub1 = serializers.SerializerMethodField()
    # pub1 = serializers.StringRelatedField(many=False, source='publisher')
    # tag1 = serializers.StringRelatedField(many=True, source='tags')
    tag1 = serializers.SerializerMethodField()

    genre = GenreSerializer()

    def get_tag1(self, obj):
        list1 = []
        for i in obj.tags.all():
            list1.append(i.title)

        return list1

    def get_genre_title(self, obj):
        return obj.genre.title

    def get_pub1(self, obj):
        return obj.publisher.title

    class Meta:
        model = Book
        fields = ['id', 'title', 'autor', 'genre', 'genre_title', 'publisher', 'pub1', 'tag1']
