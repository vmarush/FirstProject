"""
URL configuration for first project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from .views import *
from books.views import books, get_book, get_genre_books, get_tag_books, add_book,search_book
from films.views import films
from posts.views import posts, get_post, get_tag_posts, add_post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', first),
    path('second/', second),
    path('third/', third),
    path('get_books/', books, name="books"),
    path('films/', films),

    path('posts/', posts, name="posts"),
    path('posts/<int:id>/', get_post, name="get_post"),
    path('posts/tag/<str:title>/', get_tag_posts, name="get_tag_post"),

    path('get_books/<int:id>/', get_book, name="get_book"),
    path('get_genre/<str:title>/', get_genre_books, name="get_genre"),
    path('get_tag/<str:title>/', get_tag_books, name="get_tag_books"),

    path('add_book/', add_book, name="add_book"),
    path('search_book/', search_book, name="search_book"),

    path('add_post/', add_post, name="add_post")
]
