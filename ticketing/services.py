from django.db import transaction
from django.core.exceptions import ValidationError

from .models import Booking


@transaction.atomic
def create_booking(user, showtime, seat_count):
    showtime.refresh_from_db()

    if seat_count > showtime.free_seats:
        raise ValidationError("Not enough available seats.")

    booking = Booking.objects.create(
        user=user,
        showtime=showtime,
        seat_count=seat_count,
        total_price=seat_count * showtime.price,
    )

    showtime.free_seats -= seat_count
    showtime.save(update_fields=["free_seats"])

    return booking
