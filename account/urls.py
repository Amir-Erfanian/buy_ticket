from django.urls import path

from . import views

urlpatterns = [
    path(
        "register/",
        views.register_view,
        name="register",
    ),
    path(
        "login/",
        views.login_view,
        name="login",
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout",
    ),
        path(
        "profile/",
        views.profile,
        name="profile",
    ),
    path(
        "my-bookings/",
        views.my_bookings,
        name="my_bookings",
    ),
]
