from .models import Movie


def get_movies():
    return Movie.objects.all()


def get_movie(pk):
    return Movie.objects.select_related().get(pk=pk)
