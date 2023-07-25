from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Post, CategoryPost


class PostsSerializer(ModelSerializer):
    category = serializers.SerializerMethodField()
    tag1 = serializers.SerializerMethodField()
    categor_post1 = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_tag1(self, obj):
        list1 = []
        for i in obj.tags.all():
            list1.append(i.title)

        return list1

    def get_categor_post1(self, obj):
        return obj.category_post.title

    def get_category(self, obj):
        return obj.category.title

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'user', 'category', 'categor_post1', 'tag1', 'likes']


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

        fields = ['id', 'title', 'posts', 'posts1']

