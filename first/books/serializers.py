from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Book, Genre, Publisher


class CreateBookSerializer(ModelSerializer):
    tags_ids = serializers.CharField()
    def validate_tags_ids(self,value:str):
        value = value.split(', ')
        return 'Теги'
    
    class Meta:
        model = Book
        fields = ['title', 'autor', 'year', 'raiting','price','genre','tags_ids']





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


class GenreSerializerTest(ModelSerializer):

    # books = GenreBookSerializer(many=True)

    class Meta:
        model = Genre
        fields = ['id', 'title']

class PublisherBookSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ['id','title','language']


class BookSerializer(ModelSerializer):
    genre_title = serializers.SerializerMethodField()
    publisher_title = serializers.SerializerMethodField()
    # pub1 = serializers.StringRelatedField(many=False, source='publisher')
    # tag1 = serializers.StringRelatedField(many=True, source='tags')
    tag1 = serializers.SerializerMethodField()

    # genre = GenreSerializer()

    def get_tag1(self, obj):
        list1 = []
        for i in obj.tags.all():
            list1.append(i.title)

        return list1

    def get_genre_title(self, obj):
        # if obj.genre is not None:
        #     return obj.genre.title
        # return 'нет жанра'
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
        fields = ['id', 'title', 'autor', 'genre_title', 'publisher_title', 'tag1']
