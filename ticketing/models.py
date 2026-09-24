from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
import uuid


class Movie(models.Model):
    name = models.CharField(max_length=100)
    director = models.CharField(max_length=50)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1888)])
    length = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

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
    image = models.ImageField(upload_to="cinemas/", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

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

    movie = models.ForeignKey(
        Movie, on_delete=models.PROTECT, related_name="showtimes"
    )

    cinema = models.ForeignKey(
        Cinema, on_delete=models.PROTECT, related_name="showtimes"
    )

    start_time = models.DateTimeField()
    price = models.PositiveIntegerField()
    salable_seats = models.PositiveIntegerField()
    free_seats = models.PositiveIntegerField(default=0)
    rows = models.PositiveSmallIntegerField(default=5)
    seats_per_row = models.PositiveSmallIntegerField(default=10)
    status = models.IntegerField(choices=STATUS_CHOICES, default=SALE_NOT_STARTED)

    class Meta:
        ordering = ["start_time"]

    def clean(self):
        super().clean()


        if (
            self.cinema is not None
            and self.salable_seats is not None
            and self.salable_seats > self.cinema.capacity
        ):
            raise ValidationError("Salable seats exceed cinema capacity.")

        if (
            self.salable_seats is not None
            and self.free_seats is not None
            and self.free_seats > self.salable_seats
        ):
            raise ValidationError("Invalid number of free seats.")

    def save(self, *args, **kwargs):
        # On creation, free_seats should start equal to salable_seats.
        if self._state.adding and not self.free_seats:
            self.free_seats = self.salable_seats
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movie} - {self.cinema}"


class Seat(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        BOOKED = "booked", "Booked"

    showtime = models.ForeignKey(
        ShowTime,
        on_delete=models.CASCADE,
        related_name="seats",
    )

    row = models.CharField(max_length=2)
    number = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    class Meta:
        ordering = ["row", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["showtime", "row", "number"],
                name="unique_seat_per_showtime",
            )
        ]

    @property
    def is_reserved(self):
        return self.booking_seats.exists()

    def __str__(self):
        return f"{self.row}{self.number}"


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELED = "canceled", "Canceled"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    showtime = models.ForeignKey(
        ShowTime,
        on_delete=models.CASCADE,
        related_name="bookings",
    )

    booking_code = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-booked_at"]

    @property
    def total_price(self):
        return self.booking_seats.count() * self.showtime.price

    @property
    def seat_count(self):
        return self.booking_seats.count()

    def __str__(self):
        return str(self.booking_code)


class BookingSeat(models.Model):
    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="booking_seats",
    )

    seat = models.ForeignKey(
        Seat,
        on_delete=models.PROTECT,
        related_name="booking_seats",
    )

    booked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["seat"],
                name="unique_booked_seat",
            )
        ]

    def __str__(self):
        return f"{self.booking.booking_code} - {self.seat}"