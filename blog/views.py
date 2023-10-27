from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from .models import Post
from .forms import EmailPostForm

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


class postListView(ListView):
    """
    List all Posts using Class Based View
    """

    model = Post
    paginate_by = 3
    context_object_name = "posts"
    template_name = "blog/post/listCBV.html"


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


def postShare(request, year, month, day, post):
    # Retrive Post from database
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    isSent = False

    if request.method == "POST":
        # Form is submitted successfully
        form = EmailPostForm(request.POST)
        if form.is_valid():
            formData = form.cleaned_data
            postURL = request.build_absolute_uri(post.get_absolute_url())
            emailSubject = f"{formData['name']} Recommend you to read {post.title}"
            emailMessage = f"Read {formData['name']} at {postURL}\n{formData['name']}'s comments: {formData['comments']}"
            send_mail(
                subject=emailSubject,
                message=emailMessage,
                from_email="abdallah10kamal@gmail.com",
                recipient_list=[formData["to"]],
            )
            isSent = True
    else:
        form = EmailPostForm()

    # Return to template
    context = {
        "post": post,
        "form": form,
        "isSent": isSent,
    }
    return render(request, "blog/post/postShare.html", context=context)
