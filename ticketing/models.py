from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


class Movie(models.Model):
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1888)])
    length = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()

    poster = models.ImageField(
        upload_to="posters/",
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cinema(models.Model):
    cinema_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30, default="Tehran")
    capacity = models.PositiveIntegerField()
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField()

    class Meta:
        ordering = ["city", "name"]

    def __str__(self):
        return self.name


class ShowTime(models.Model):

    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6

    STATUS_CHOICES = (
        (SALE_NOT_STARTED, "Sale Not Started"),
        (SALE_OPEN, "On Sale"),
        (TICKETS_SOLD, "Sold Out"),
        (SALE_CLOSED, "Closed"),
        (MOVIE_PLAYED, "Played"),
        (SHOW_CANCELED, "Canceled"),
    )

    movie = models.ForeignKey(Movie, on_delete=models.PROTECT, related_name="showtimes")

    cinema = models.ForeignKey(
        Cinema, on_delete=models.PROTECT, related_name="showtimes"
    )

    start_time = models.DateTimeField()

    price = models.PositiveIntegerField()

    salable_seats = models.PositiveIntegerField()

    free_seats = models.PositiveIntegerField()

    rows = models.PositiveSmallIntegerField(default=5)

    seats_per_row = models.PositiveSmallIntegerField(default=10)

    status = models.IntegerField(choices=STATUS_CHOICES, default=SALE_NOT_STARTED)

    class Meta:
        ordering = ["start_time"]

    def clean(self):
        if self.salable_seats > self.cinema.capacity:
            raise ValidationError("Salable seats exceed cinema capacity.")

        if self.free_seats > self.salable_seats:
            raise ValidationError("Invalid number of free seats.")

    def __str__(self):
        return f"{self.movie} - {self.cinema}"


class Seat(models.Model):
    showtime = models.ForeignKey(
        ShowTime,
        on_delete=models.CASCADE,
        related_name="seats",
    )

    row = models.CharField(max_length=1)

    number = models.PositiveIntegerField()

    is_reserved = models.BooleanField(default=False)

    class Meta:
        unique_together = ("showtime", "row", "number")
        ordering = ["row", "number"]

    def __str__(self):
        return f"{self.row}{self.number}"


class Booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")

    showtime = models.ForeignKey(
        ShowTime, on_delete=models.CASCADE, related_name="bookings"
    )

    seats = models.ManyToManyField(Seat, related_name="bookings")

    total_price = models.PositiveIntegerField()

    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booked_at"]

    @property
    def seat_count(self):
        return self.seats.count()

    def __str__(self):
        return f"{self.user.username} | {self.showtime.movie}"
