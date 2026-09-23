from django.shortcuts import render, get_object_or_404
from django.db.models import Q, F
from .models import BlogPost


def posts_view(request, cat_name=None, author_username=None, **kwargs):
    posts = BlogPost.objects.filter(is_active=True, is_deleted=False)

    if cat_name:
        posts = posts.filter(category__name=cat_name)
    if author_username:
        posts = posts.filter(author__username=author_username)

    return render(request, "blog/posts_page.html", {
        "posts": posts,
        "cat_name": cat_name,
        "author_username": author_username,
    })


def post_detail_view(request, slug):
    post = get_object_or_404(
        BlogPost, slug=slug, is_active=True, is_deleted=False
    )

    # Increment view count atomically
    BlogPost.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
    post.refresh_from_db(fields=["view_count"])

    related_posts = (
        BlogPost.objects.filter(
            category__in=post.category.all(),
            is_active=True,
            is_deleted=False,
        )
        .exclude(pk=post.pk)
        .distinct()[:3]
    )

    return render(request, "blog/post_detail_page.html", {
        "post": post,
        "related_posts": related_posts,
    })


def blog_search(request):
    query = request.GET.get("s", "").strip()
    posts = BlogPost.objects.filter(is_active=True, is_deleted=False)

    if query:
        posts = posts.filter(
            Q(content__icontains=query)
            | Q(title__icontains=query)
            | Q(author__username__icontains=query)
        ).distinct()

    context = {
        "posts": posts,
        "query": query,
        "post_count": posts.count(),
    }
    return render(request, "blog/posts_page.html", context)