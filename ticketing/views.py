from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BookingForm, RegisterForm
from .models import Booking, Cinema, Movie, Seat, ShowTime


def movie_list(request):
    movies = Movie.objects.all()

    return render(
        request,
        "ticketing/movie_list.html",
        {
            "movies": movies,
        },
    )


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(
        request,
        "ticketing/movie_detail.html",
        {
            "movie": movie,
        },
    )


def cinema_list(request):
    cinemas = Cinema.objects.all()
    return render(
        request,
        "ticketing/cinema_list.html",
        {
            "cinemas": cinemas,
        },
    )


def register(request):
    if request.user.is_authenticated:
        return redirect("movie_list")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(request, "Your account has been created successfully.")
            return redirect("movie_list")

    else:
        form = RegisterForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


@login_required
def profile(request):
    return render(
        request,
        "registration/profile.html",
    )


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .prefetch_related("seats")
        .select_related(
            "showtime",
            "showtime__movie",
            "showtime__cinema",
        )
        .order_by("-booked_at")
    )

    return render(
        request,
        "registration/my_bookings.html",
        {
            "bookings": bookings,
        },
    )


@login_required
def book_ticket(request, showtime_id):
    showtime = get_object_or_404(
        ShowTime,
        pk=showtime_id,
    )

    available_seats = Seat.objects.filter(
        showtime=showtime,
        is_reserved=False,
    ).order_by("row", "number")

    seat_choices = [
        (
            seat.id,
            f"{seat.row}{seat.number}",
        )
        for seat in available_seats
    ]

    if request.method == "POST":

        form = BookingForm(
            request.POST,
            seat_choices=seat_choices,
        )

        if form.is_valid():

            selected_ids = form.cleaned_data["seats"]

            with transaction.atomic():

                seats = Seat.objects.select_for_update().filter(
                    id__in=selected_ids,
                    showtime=showtime,
                    is_reserved=False,
                )

                if seats.count() != len(selected_ids):
                    messages.error(
                        request,
                        "One or more selected seats have just been reserved by another user.",
                    )

                    return redirect(
                        "book_ticket",
                        showtime_id=showtime.id,
                    )

                booking = Booking.objects.create(
                    user=request.user,
                    showtime=showtime,
                    total_price=showtime.price * seats.count(),
                )

                booking.seats.set(seats)

                seats.update(
                    is_reserved=True,
                )

                showtime.free_seats -= seats.count()

                if showtime.free_seats <= 0:
                    showtime.free_seats = 0
                    showtime.status = ShowTime.TICKETS_SOLD

                showtime.save()

            messages.success(request, "Your booking has been completed successfully.")

            return redirect("my_bookings")

    else:

        form = BookingForm(
            seat_choices=seat_choices,
        )

    reserved_seats = Seat.objects.filter(
        showtime=showtime,
        is_reserved=True,
    ).order_by("row", "number")

    context = {
        "showtime": showtime,
        "form": form,
        "available_seats": available_seats,
        "reserved_seats": reserved_seats,
    }

    return render(
        request,
        "ticketing/book_ticket.html",
        context,
    )
