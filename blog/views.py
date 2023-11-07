from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from blog.models import Post
from blog.forms import EmailPostForm, CommentForm
from taggit.models import Tag

# Create your views here.


def home(request):
    return render(request, "blog/home.html")


def about(request):
    return render(request, "blog/about.html")


def postList(request, tagSlug=None):
    allPosts = Post.objects.all()

    tags = None
    if tagSlug:
        tags = get_object_or_404(Tag, slug=tagSlug)
        allPosts = allPosts.filter(tags__in=[tags])

    paginator = Paginator(allPosts, 3)
    pageNumber = request.GET.get("page", 1)

    try:
        posts = paginator.page(pageNumber)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        posts = paginator.page(1)

    context = {
        "posts": posts,
        "tags": tags,
    }

    return render(request, "blog/post/list.html", context)


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

    comments = post.comments.filter(active=True)

    postTagsIDs = post.tags.values_list("id", flat=True)
    postsWithSameTags = Post.objects.filter(tags__in=postTagsIDs).exclude(id=post.id)
    postsWithSameTags = postsWithSameTags.annotate(same_tags=Count("tags")).order_by(
        "-same_tags", "-publish"
    )

    context = {
        "post": post,
        "comments": comments,
        "form": CommentForm(),
        "postsWithSameTags": postsWithSameTags,
    }
    return render(request, "blog/post/detail.html", context)


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


@require_POST
def postComment(request, year, month, day, post):
    # Get Post from database
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    comment = None

    # Get Data From POST request as formData
    formData = CommentForm(request.POST)

    # Check if formData is_valid and save if valid
    if formData.is_valid():
        # link comment with thier post and save
        comment = formData.save(commit=False)
        comment.post = post
        comment.save()

    context = {
        "post": post,
        "form": formData,
        "comment": comment,
    }
    return render(request, "blog/post/postComment.html", context=context)
