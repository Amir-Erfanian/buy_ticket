from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور",
                "autocomplete": "new-password",
            }
        )
    )

    password2 = forms.CharField(
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "تکرار رمز عبور",
                "autocomplete": "new-password",
            }
        )
    )

    class Meta:
        model = User
        fields = ("email",)

        widgets = {
            "email": forms.EmailInput(
                attrs={
                    "placeholder": "ایمیل خود را وارد کنید",
                    "autocomplete": "email",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "این ایمیل قبلاً ثبت نام کرده است."
            )

        return email

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "رمزهای عبور یکسان نیستند."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["email"]
        user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "placeholder": "ایمیل خود را وارد کنید",
                "autocomplete": "email",
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور",
                "autocomplete": "current-password",
            }
        )
    )

