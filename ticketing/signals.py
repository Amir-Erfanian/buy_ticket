from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ShowTime, Seat


@receiver(post_save, sender=ShowTime)
def create_seats(sender, instance, created, **kwargs):

    if not created:
        return

    rows = ["A", "B", "C", "D", "E"]

    for row in rows:

        for number in range(1, 11):

            Seat.objects.create(
                showtime=instance,
                row=row,
                number=number,
            )
