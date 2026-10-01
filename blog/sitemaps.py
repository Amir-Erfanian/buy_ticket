from django.contrib.sitemaps import Sitemap
from blog.models import BlogPost


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return BlogPost.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.publish_date
