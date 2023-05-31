from django.shortcuts import render

from .models import Post, PostTag, Category


def posts(request):
    posts = Post.objects.all()
    posttag = PostTag.objects.all()
    category = Category.objects.all()

    return render(request, template_name="index1.html", context={
        "posts": posts,
        "posttag": posttag,
        "category": category})
