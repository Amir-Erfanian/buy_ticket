from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import ContactForm



def home_view(request):
    return render(request, "core/home_page.html")


def about_view(request):
    return render(request, "core/about_page.html")


def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "پیام شما با موفقیت ارسال شد. ممنون از تماس شما!")
            return redirect("contact_page")
        else:
            messages.error(request, "لطفاً خطاهای فرم را برطرف کنید.")
    else:
        form = ContactForm()

    return render(request, "core/contact_page.html", {"form": form})