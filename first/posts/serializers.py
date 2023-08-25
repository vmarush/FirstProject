import requests
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, CategoryPost


class CreatePostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_post",
            "likes",
            "user",
        ]


class PostsSerializer(ModelSerializer):
    category = serializers.SerializerMethodField()
    tag_title = serializers.SerializerMethodField()
    category_post = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_tag_title(self, obj):
        list1 = []
        for i in obj.tags.all():
            list1.append(i.title)

        return list1

    def get_category_post(self, obj):
        return obj.category_post.title

    def get_category(self, obj):
        return obj.category.title

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "user",
            "category",
            "category_post",
            "tag_title",
            "likes",
        ]


class PostsSerializer1(ModelSerializer):
    category = serializers.SerializerMethodField()
    tag_title = serializers.SerializerMethodField()
    category_post = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_tag_title(self, obj):
        list1 = []
        for i in obj.tags.all():
            list1.append(i.title)

        return list1

    def get_category_post(self, obj):
        try:
            return obj.category_post.title
        except AttributeError:
            return "нет категории поста"

    def get_category(self, obj):
        try:
            return obj.category.title
        except AttributeError:
            return "категория отстутсвует"

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "description",
            "category",
            "category_post",
            "tag_title",
            "likes",
            "user",
        ]


# class PostsSerializer(ModelSerializer):
#     category = serializers.StringRelatedField(many=False)
#     tags = serializers.StringRelatedField(many=True,)
#
#     class Meta:
#         model = Post
#         fields = ['id', 'title','description' ,'user', 'category', 'tags','likes']


class CatPostSerializer(ModelSerializer):
    posts1 = serializers.SerializerMethodField()

    def get_posts1(self, obj):
        list1 = []
        print(obj.posts.all())
        for i in obj.posts.all():
            print(i.title)
            list1.append(i.title)
        return list1

    class Meta:
        model = CategoryPost

        fields = ["id", "title", "posts", "posts1"]
