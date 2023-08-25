from django.urls import path
from posts.views import (
    get_tag_posts,
    add_post,
    search_post,
    search_category_post,
    delete_post,
    update_post,
    likes_post,
    PostListView,
    PostDetailView,
    polychit_post,
    polychit_cat_post,
    PostAPIView,
    create_post_for_json,
)

urlpatterns = [
    # path('posts/', posts, name="posts"),
    # path('posts/<int:id>/', get_post, name="get_post"),
    path("update_post/<int:id>/", update_post, name="update_post"),
    path("posts/tag/<str:title>/", get_tag_posts, name="get_tag_post"),
    path("add_post/", add_post, name="add_post"),
    path("search_posts/", search_post, name="search_post"),
    path("search_category_post/", search_category_post, name="search_category_post"),
    path("delete_post/<int:id>/", delete_post, name="delete_post"),
    path("likes_post/<int:id>/", likes_post, name="likes_post"),
    path("posts/", PostListView.as_view(), name="posts"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="get_post"),
    path("polychit_post/<int:id>/", polychit_post, name="polychit_post"),
    path("polychit_cat_post/<int:id>/", polychit_cat_post, name="polychit_cat_post"),
    path("test_all/", PostAPIView.as_view()),
    path("create_post_for_json/", create_post_for_json),
]
