from django import template
from blog.models import Post

register = template.Library()


@register.simple_tag
def totalPosts():
    return Post.objects.count()


@register.inclusion_tag("blog/post/latestPosts.html")
def showLatestPosts(count=5):
    latestPosts = Post.objects.order_by("-publish")[:count]
    return {"latestPosts": latestPosts}
