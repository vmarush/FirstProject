from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, PostTag, Category, CategoryPost
from django.http import HttpResponse

from .forms import PostForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.migrations import serializer
from django.http import JsonResponse

from .serializers import (
    PostsSerializer,
    CatPostSerializer,
    CreatePostSerializer,
    PostsSerializer1,
)
from rest_framework.decorators import api_view


def polychit_post(request, id):
    try:
        posti = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse(f"<h1> 404 </h1>")
    serializer = PostsSerializer(posti)

    return JsonResponse(data=serializer.data)


def polychit_cat_post(request, id):
    try:
        posti = CategoryPost.objects.get(id=id)
    except CategoryPost.DoesNotExist:
        return HttpResponse(f"<h1> 404 </h1>")
    serializer = CatPostSerializer(posti)

    return JsonResponse(data=serializer.data)


@api_view(
    [
        "POST",
    ]
)
def create_post_for_json(request):
    print(request.POST)
    serializer = CreatePostSerializer(data=request.POST)
    if serializer.is_valid():
        print("ok")
    else:
        print(serializer.errors)
        return JsonResponse(data=serializer.errors)
    post = Post.objects.create(**serializer.validated_data)
    serializer = PostsSerializer1(post)
    return JsonResponse(data=serializer.data)


class PostAPIView(APIView):
    def get(self, request):
        post = Post.objects.all().values()
        return Response({"post": list(post)})


class PostListView(ListView):
    model = Post
    context_object_name = "posts1"
    template_name = "templates/index1.html"
    queryset = Post.objects.all()


# def posts(request):
#     posts = Post.objects.all()
#     posttag = PostTag.objects.all()
#     category = Category.objects.all()
#
#     return render(request, template_name="index1.html", context={
#         "posts": posts,
#         "posttag": posttag,
#         "category": category})


class PostDetailView(DetailView):
    model = Post
    template_name = "templates/detailinfopost.html"
    context_object_name = "post"


# def get_post(request, id):
#     try:
#         post = Post.objects.get(id=id)
#     except Post.DoesNotExist:
#         return HttpResponse(f"поста с таким  {id} нету")
#     return render(request, "templates/detailinfopost.html", context={"post": post})


def get_tag_posts(request, title):
    try:
        posttags = PostTag.objects.get(title=title)
    except PostTag.DoesNotExist:
        return HttpResponse(f"Тега  {title} нету")
    return render(request, "templates/tegikpostam.html", context={"tagpost": posttags})


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            form = PostForm()
            return render(request, "add_post.html", context={"form": form})
        elif request.method == "POST":
            category_id = request.POST["category"]
            category_post_id = request.POST["category_post"]
            if category_id != "":
                category = Category.objects.get(id=category_id)
            else:
                category = None
            if category_post_id != "":
                category_post = CategoryPost.objects.get(id=category_post_id)
            else:
                category_post = None

            image = request.FILES.get("image", "123.jpg")

            post = Post.objects.create(
                title=request.POST["title"],
                description=request.POST["description"],
                category_post=category_post,
                category=category,
                image=image,
                user=request.user,
            )
            tags = request.POST.getlist("tags")
            post.tags.set(tags)
            post.save()

            return redirect("posts")
    else:
        return HttpResponse(f"<h1>у вас нет прав</h1>")


def search_post(request):
    post = request.GET["post"]
    posts = Post.objects.filter(title__contains=post)

    return render(request, "search_post.html", context={"posts": posts})


def search_category_post(request):
    title = request.GET["title"]

    posts = Post.objects.all()

    if title != "":
        posts = posts.filter(category_post__title__contains=title)

    return render(request, "search_category_post.html", context={"posts": posts})


def delete_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse(f"<h1>поста с таким айди {id} не существует</h1>")
    if request.user.username != post.user.username:
        return HttpResponse(f"<h1>у вас нет прав</h1>")
    else:
        post.delete()

        return redirect("posts")


def update_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse(f"<h1>поста с таким айди {id} не существует</h1>")
    if request.user.username != post.user.username:
        return HttpResponse(f"<h1>у вас нет прав</h1>")
    else:
        if request.method == "GET":
            form = PostForm(instance=post)
            return render(
                request, "update_post.html", context={"post": post, "form": form}
            )
        else:
            category_id = request.POST["category"]
            category_post_id = request.POST["category_post"]
            if category_id != "":
                category = Category.objects.get(id=category_id)
            else:
                category = None
            if category_post_id != "":
                category_post = CategoryPost.objects.get(id=category_post_id)
            else:
                category_post = None

            image = request.FILES.get("image", "123.jpg")

            post.title = request.POST["title"]
            post.description = request.POST["description"]
            post.category_post = category_post
            post.category = category
            post.image = image

            tags = request.POST.getlist("tags")
            post.tags.set(tags)
            post.save()

        return redirect("get_post", id=post.id)


def likes_post(request, id):
    try:
        post = Post.objects.get(pk=id)

    except Post.DoesNotExist:
        return HttpResponse(f"<h1>такого поста нету </h1>")
    if request.user.is_authenticated:
        post.likes = post.likes + 1
        post.save()
        return redirect("get_post", pk=post.id)
