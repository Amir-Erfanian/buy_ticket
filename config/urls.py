from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSiteMap

sitemaps = {
    'static': StaticViewSiteMap
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("account.urls")),
    path("", include("core.urls")),
    path("blog/", include("blog.urls")),
    path("", include("ticketing.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
)
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

handler404 = 'config.views.custom_page_not_found'
