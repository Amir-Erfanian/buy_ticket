from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "مثلاً: علی رضایی",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "example@email.com",
                "dir": "ltr",
            }),
            "subject": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "موضوع پیام شما",
            }),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "پیام خود را اینجا بنویسید...",
            }),
        }
        error_messages = {
            "name": {"required": "لطفاً نام خود را وارد کنید."},
            "email": {
                "required": "لطفاً ایمیل خود را وارد کنید.",
                "invalid": "ایمیل وارد شده معتبر نیست.",
            },
            "subject": {"required": "لطفاً موضوع پیام را وارد کنید."},
            "message": {"required": "لطفاً متن پیام را وارد کنید."},
        }