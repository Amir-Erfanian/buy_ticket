from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm
from ticketing.models import Booking


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
        "account/profile.html",
    )


@login_required
def my_bookings(request):
    bookings = (
        Booking.objects.filter(user=request.user)
        .select_related(
            "showtime",
            "showtime__movie",
            "showtime__cinema",
        )
        .prefetch_related(
            "booking_seats__seat",
        )
    )

    return render(
        request,
        "account/my_bookings.html",
        {
            "bookings": bookings,
        },
    )
