from django.urls import path
from posts.views import posts, get_post, get_tag_posts, add_post, search_post, search_category_post, delete_post,update_post

urlpatterns = [
    path('posts/', posts, name="posts"),
    path('posts/<int:id>/', get_post, name="get_post"),
    path('update_post/<int:id>/', update_post, name="update_post"),

    path('posts/tag/<str:title>/', get_tag_posts, name="get_tag_post"),
    path('add_post/', add_post, name="add_post"),
    path('search_posts/', search_post, name="search_post"),
    path('search_category_post/', search_category_post, name="search_category_post"),
    path('delete_post/<int:id>/', delete_post, name="delete_post"),

]
