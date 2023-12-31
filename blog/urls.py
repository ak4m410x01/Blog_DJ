from django.urls import path
from . import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("post/list/", views.postList, name="postList"),
    path("post/list/tag/<slug:tagSlug>/", views.postList, name="postList-tag"),
    path(
        "post/<int:year>/<int:month>/<int:day>/<slug:post>/",
        views.postDetail,
        name="postDetail",
    ),
    path("post/list/cbv/", views.postListView.as_view(), name="postListView"),
    # Share Post
    path(
        "post/<int:year>/<int:month>/<int:day>/<slug:post>/share/",
        views.postShare,
        name="postShare",
    ),
    # Comment on Post
    path(
        "post/<int:year>/<int:month>/<int:day>/<slug:post>/comment/",
        views.postComment,
        name="postComment",
    ),
]
