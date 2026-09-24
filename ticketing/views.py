from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from .forms import BookingForm, SeatSelectionForm
from .models import Booking, Cinema, Movie, Seat, ShowTime
from .services import create_booking
from django.db.models import Q

def movie_list(request):
    query = request.GET.get("q", "").strip()
    movies = Movie.objects.filter(is_active=True)

    if query:
        movies = movies.filter(
            Q(name__icontains=query)
            | Q(director__icontains=query)
            | Q(description__icontains=query)
        ).distinct()

    return render(request, "ticketing/movie_list.html", {
        "movies": movies,
        "query": query,
        "movie_count": movies.count(),
    })

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


@login_required
def select_seats(request, pk):
    showtime = get_object_or_404(ShowTime, pk=pk)

    seats = showtime.seats.filter(status=Seat.Status.AVAILABLE)

    if request.method == "POST":
        form = SeatSelectionForm(
            request.POST,
            seat_queryset=seats,
        )

        if form.is_valid():
            booking = create_booking(
                user=request.user,
                showtime=showtime,
                seat_ids=[int(i) for i in form.cleaned_data["seats"]],
            )

            return redirect(
                "booking_detail",
                booking.booking_code,
            )

    else:
        form = SeatSelectionForm(
            seat_queryset=seats,
        )

    return render(
        request,
        "ticketing/select_seats.html",
        {
            "showtime": showtime,
            "form": form,
        },
    )

