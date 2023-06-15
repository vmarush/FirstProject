from django.shortcuts import render, redirect

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




def add_post(request):
    if request.method == "GET":
        form = PostForm()
        return render(request, "add_post.html", context={"form": form})
    elif request.method == "POST":
        category_id = request.POST['category']
        date_create_post = request.POST['date_create']

        if category_id != '' and date_create_post != '':
            category = Category.objects.get(id=category_id)
            date_create = request.Post['date_create']

        else:
            category = None
            date_create = None

        post = Post.objects.create(title=request.POST['title'],
                                   description=request.POST['description'],
                                   date_create=date_create,
                                   category=category,
                                   )
        tags = request.POST.getlist('tags')
        post.tags.set(tags)
        post.save()

        return redirect("posts")


def search_post(request):
    search_query = request.GET['search']
    posts = Post.objects.filter(title__contains=search_query)

    return render(request, 'search_post.html', context={"posts": posts})