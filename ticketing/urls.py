from django.urls import path
from .views import (
    movie_detail,
    movie_list,
    cinema_list,
    book_ticket,
    select_seats,
)

urlpatterns = [
    path(
        "movies/",
        movie_list,
        name="movie_list",
    ),
    path(
        "movies/<int:pk>/",
        movie_detail,
        name="movie_detail",
    ),
    path(
        "cinemas/",
        cinema_list,
        name="cinema_list",
    ),
    path(
        "book/<int:showtime_id>/",
        book_ticket,
        name="book_ticket",
    ),
    path(
        "showtimes/<int:pk>/seats/",
        select_seats,
        name="select_seats",
    ),
]
