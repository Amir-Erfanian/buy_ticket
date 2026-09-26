from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import RegisterForm, LoginForm


def register_view(request):

    if request.user.is_authenticated:
        return redirect("home_page")

    if request.method == "POST":

        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "حساب کاربری شما با موفقیت ایجاد شد."
            )

            return redirect("home_page")

    else:
        form = RegisterForm()

    return render(
        request,
        "account/register.html",
        {
            "form": form,
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect("home_page")

    if request.method == "POST":

        form = LoginForm(request.POST)

        if form.is_valid():

            email = form.cleaned_data["email"].lower()
            password = form.cleaned_data["password"]

            user = authenticate(
                request,
                username=email,
                password=password,
            )

            if user is not None:

                login(request, user)

                messages.success(
                    request,
                    "با موفقیت وارد شدید."
                )

                next_url = request.GET.get("next")

                if next_url:
                    return redirect(next_url)

                return redirect("home_page")

            form.add_error(
                None,
                "ایمیل یا رمز عبور اشتباه است."
            )

    else:
        form = LoginForm()

    return render(
        request,
        "account/login.html",
        {
            "form": form,
        }
    )


def logout_view(request):
    logout(request)
    messages.success(
        request,
        "با موفقیت از حساب کاربری خارج شدید."
    )
    return redirect("home_page")

