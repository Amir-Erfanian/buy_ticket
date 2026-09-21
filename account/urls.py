from django.urls import path
from django.contrib.auth import views as auth_views


from .views import register, profile, my_bookings

urlpatterns = [
    path(
        "register/",
        register,
        name="register",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "profile/",
        profile,
        name="profile",
    ),
    path(
        "my-bookings/",
        my_bookings,
        name="my_bookings",
    ),
]
