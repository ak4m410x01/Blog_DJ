from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post

# Create your views here.


def home(request):
    return render(request, "blog/home.html")


def about(request):
    return render(request, "blog/about.html")


def postList(request):
    allPosts = Post.objects.all()
    paginator = Paginator(allPosts, 3)
    pageNumber = request.GET.get("page", 1)

    try:
        posts = paginator.page(pageNumber)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    return render(request, "blog/post/list.html", {"posts": posts})


def postDetail(request, year, month, day, post):
    # Method 1
    # try:
    #     post = Post.objects.get(id=id)
    # except Post.DoesNotExist:
    #     return Http404("No Post Found.")

    # Method 2
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )

    return render(request, "blog/post/detail.html", {"post": post})
