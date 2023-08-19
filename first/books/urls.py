from django.urls import path

from books.views import (
    get_genre_books,
    get_tag_books,
    add_book,
    search_book,
    delete_book,
    update_book,
    add_comment,
    buy_book,
    favorite_book,
    favorites,
    get_all_comments,
    delete_from_favorites,
    BookListView,
    BookDetailView, search_book_by_tags, book_detail, get_all_books, create_book, get_all_genre, get_all_publishers,
    update_book_api, delete_book_api, BookViewSet
)
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register('books', BookViewSet)

urlpatterns = [
    path("get_genre/<str:title>/", get_genre_books, name="get_genre"),
    path("get_tag/<str:title>/", get_tag_books, name="get_tag_books"),
    path("add_book/", add_book, name="add_book"),
    path("update_book/<int:id>/", update_book, name="update_book_by_id"),
    path("add_comment/<int:id>/", add_comment, name="add_comment"),
    path("search_book/", search_book, name="search_book"),
    path("delete_book/<int:id>/", delete_book, name="delete_book"),
    path("buy_book/<int:id>/", buy_book, name="buy_book"),
    path("favorite/<int:id>/", favorite_book, name="favorite_book"),
    path("favorites/", favorites, name="favorites"),
    path("delete_from_favorites/<int:id>/", delete_from_favorites, name="delete_from_favorites"),
    path("get_books/", BookListView.as_view(), name="books"),
    path("detail_book/<int:pk>/", BookDetailView.as_view(), name='get_book'),
    path("search_book_by_tags/", search_book_by_tags, name='search_book_by_tags'),
    # path("book_detail/", book_detail, name='book_detail'),
    path("get_all_books/", get_all_books, name='get_all_books'),
    path("get_book/<int:id>/", book_detail),
    path("create_book/", create_book),
    path("get_all_genre/", get_all_genre),
    path("get_all_publishers/", get_all_publishers),
    path("update_book_api/<int:id>/", update_book_api),
    path('delete_book_api/<int:id>/', delete_book_api),
    path('get_all_comment', get_all_comments)

]
urlpatterns += router.urls
