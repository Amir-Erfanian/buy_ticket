from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_posts")
    slug = models.SlugField(unique=True, blank=True)
    category = models.ManyToManyField(Category, related_name="posts")
    view_count = models.IntegerField(default=0, blank=True, null=True)
    image = models.ImageField(upload_to="blogs/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.author}"

    def get_absolute_url(self):
        return reverse("blog:post_detail_page", kwargs={"slug": self.slug})

@receiver(pre_save, sender=BlogPost)
def generate_blog_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        base_slug = slugify(instance.title) or "post"
        slug = base_slug
        counter = 1
        while BlogPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        instance.slug = slug