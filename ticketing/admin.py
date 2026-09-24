from django.contrib import admin

from .models import (
    Movie,
    Cinema,
    ShowTime,
    Seat,
    Booking,
    BookingSeat,
)


@admin.register(BookingSeat)
class BookingSeatAdmin(admin.ModelAdmin):
    list_display = (
        "booking",
        "seat",
        "booked_at",
    )

    list_filter = ("booking__showtime",)

    search_fields = (
        "booking__booking_code",
        "seat__row",
    )


class SeatInline(admin.TabularInline):
    model = Seat
    extra = 0
    can_delete = False

    fields = (
        "row",
        "number",
        "status",
    )

    ordering = (
        "row",
        "number",
    )


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "director",
        "year",
        "length",
        "is_active"
    )

    search_fields = (
        "name",
        "director",
    )

    ordering = ("name",)


@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    list_display = (
        "cinema_code",
        "name",
        "city",
        "capacity",
        "phone",
    )

    list_filter = ("city",)

    search_fields = (
        "name",
        "city",
        "phone",
    )

    ordering = (
        "city",
        "name",
    )


@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    list_display = (
        "movie",
        "cinema",
        "start_time",
        "price",
        "status",
        "free_seats",
        "salable_seats",
    )

    list_filter = (
        "status",
        "cinema",
        "movie",
        "start_time",
    )

    search_fields = (
        "movie__name",
        "cinema__name",
    )

    autocomplete_fields = (
        "movie",
        "cinema",
    )

    ordering = ("start_time",)

    inlines = [
        SeatInline,
    ]


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "showtime",
        "row",
        "number",
        "status",
    )

    list_filter = (
        "status",
        "showtime",
    )

    search_fields = (
        "showtime__movie__name",
        "row",
    )

    ordering = (
        "showtime",
        "row",
        "number",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "showtime",
        "seat_list",
        "seat_count_display",
        "total_price",
        "booked_at",
    )

    search_fields = (
        "user__username",
        "showtime__movie__name",
        "showtime__cinema__name",
    )

    autocomplete_fields = (
        "user",
        "showtime",
    )

    readonly_fields = ("booked_at",)

    ordering = ("-booked_at",)

    @admin.display(description="Seats")
    def seat_count_display(self, obj):
        return obj.booking_seats.count()

    @admin.display(description="Seat Numbers")
    def seat_list(self, obj):
        return ", ".join(
            str(bs.seat)
            for bs in obj.booking_seats.select_related("seat").order_by(
                "seat__row", "seat__number"
            )
        )