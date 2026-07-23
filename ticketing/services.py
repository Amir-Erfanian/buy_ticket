from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Booking, BookingSeat, Seat, ShowTime


@transaction.atomic
def create_booking(*, user, showtime: ShowTime, seat_ids: list[int]) -> Booking:
    if not seat_ids:
        raise ValidationError("Please select at least one seat.")

    seats = (
        Seat.objects
        .select_for_update()
        .filter(
            id__in=seat_ids,
            showtime=showtime,
        )
    )

    if seats.count() != len(seat_ids):
        raise ValidationError("One or more selected seats are invalid.")

    booked_seats = seats.filter(
        status=Seat.Status.BOOKED,
    )

    if booked_seats.exists():
        raise ValidationError("Some selected seats are already booked.")

    booking = Booking.objects.create(
        user=user,
        showtime=showtime,
    )

    BookingSeat.objects.bulk_create(
        [
            BookingSeat(
                booking=booking,
                seat=seat,
            )
            for seat in seats
        ]
    )

    seats.update(
        status=Seat.Status.BOOKED,
    )

    return booking


@transaction.atomic
def cancel_booking(booking: Booking):
    seats = Seat.objects.filter(
        booking_seats__booking=booking,
    )

    seats.update(
        status=Seat.Status.AVAILABLE,
    )

    booking.booking_seats.all().delete()

    booking.status = Booking.Status.CANCELED
    booking.save(update_fields=["status"])