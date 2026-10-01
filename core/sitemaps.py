from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['home_page', 'about_page', 'contact_page']

    def location(self, item):
        return reverse(item)