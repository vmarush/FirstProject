from django.shortcuts import render,redirect

from .models import Post, PostTag, Category
from django.http import HttpResponse

from .forms import PostForm


def posts(request):
    posts = Post.objects.all()
    posttag = PostTag.objects.all()
    category = Category.objects.all()

    return render(request, template_name="index1.html", context={
        "posts": posts,
        "posttag": posttag,
        "category": category})


def get_post(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return HttpResponse(f"поста с таким  {id} нету")
    return render(request, "templates/detailinfopost.html", context={"post": post})


def get_tag_posts(request, title):
    try:
        posttags = PostTag.objects.get(title=title)
    except PostTag.DoesNotExist:
        return HttpResponse(f"Тега  {title} нету")
    return render(request, "templates/tegikpostam.html", context={"tagpost": posttags})


# def add_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse("<h1>пост добавлен в бд!</h1>")
#
#     else:
#         form = PostForm()
#     return render(request, "add_post.html", context={'form': form})


def add_post(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "add_post.html", context={"form": form})
    elif request.method == "POST":
        category_id = request.POST['category']

        if category_id != '':
            category = Category.objects.get(id=category_id)
        else:
            category = None

        post = Post.objects.create(title = request.POST['title'],
                            description=request.POST['description'],
                            date_create=request.POST['date_create'],
                            category=category,
                            )
        tags = request.POST.getlist('tags')
        post.tags.set(tags)
        post.save()

        return redirect("posts")
