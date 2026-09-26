from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):

    email = forms.EmailField(
        required=True,
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "ایمیل خود را وارد کنید",
                "autocomplete": "email",
                "required": True,
            }
        ),
    )

    password1 = forms.CharField(
        required=True,
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور",
                "autocomplete": "new-password",
                "required": True,
            }
        ),
    )

    password2 = forms.CharField(
        required=True,
        label="تکرار رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "تکرار رمز عبور",
                "autocomplete": "new-password",
                "required": True,
            }
        ),
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "این ایمیل قبلاً ثبت نام کرده است."
            )

        return email

    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if password:
            password_validation.validate_password(
                password,
                self.instance,
            )

        return password

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error(
                "password2",
                "رمزهای عبور یکسان نیستند."
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]

        user.set_password(
            self.cleaned_data["password1"]
        )

        # New accounts are disabled by default
        user.is_active = False

        if commit:
            user.save()

        return user


class LoginForm(forms.Form):

    email = forms.EmailField(
        required=True,
        label="ایمیل",
        widget=forms.EmailInput(
            attrs={
                "placeholder": "ایمیل خود را وارد کنید",
                "autocomplete": "email",
                "required": True,
            }
        ),
    )

    password = forms.CharField(
        required=True,
        label="رمز عبور",
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "رمز عبور",
                "autocomplete": "current-password",
                "required": True,
            }
        ),
    )

