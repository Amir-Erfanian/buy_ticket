from django.urls import path
from .views import posts_view, post_detail_view, blog_search

app_name = "blog"

urlpatterns = [
    path("", posts_view, name="posts_page"),
    path("search/", blog_search, name="search"),
    path("category/<str:cat_name>/", posts_view, name="category"),
    path("author/<str:author_username>/", posts_view, name="author"),
    path("<slug:slug>/", post_detail_view, name="post_detail_page"),
]