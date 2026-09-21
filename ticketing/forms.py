from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class BookingForm(forms.Form):
    seats = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        seat_choices = kwargs.pop("seat_choices", [])
        super().__init__(*args, **kwargs)

        self.fields["seats"].choices = seat_choices


class SeatSelectionForm(forms.Form):
    seats = forms.MultipleChoiceField(
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    def __init__(self, *args, seat_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)

        if seat_queryset is not None:
            self.fields["seats"].choices = [
                (seat.id, f"{seat.row}{seat.number}") for seat in seat_queryset
            ]
