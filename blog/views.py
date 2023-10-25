from django.shortcuts import get_object_or_404, render
from django.http import Http404
from .models import Post

# Create your views here.


def home(request):
    return render(request, "blog/home.html")


def about(request):
    return render(request, "blog/about.html")


def postList(request):
    posts = Post.objects.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def postDetail(request, id):
    # Method 1
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     return Http404("No Post Found.")

    # Method 2
    post = get_object_or_404(Post, id=id)

    return render(request, "blog/post/detail.html", {"post": post})
