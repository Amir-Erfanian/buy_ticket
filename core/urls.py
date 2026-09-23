from django.urls import path

from .views import home_view, about_view, contact_view

urlpatterns = [
    path("", home_view, name="home_page"),
    path("about/", about_view, name="about_page"),
    path("contact/", contact_view, name="contact_page"),
]
