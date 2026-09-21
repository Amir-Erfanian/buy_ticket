from django.shortcuts import render


def home_page(request):
    return render(request, "core/home_page.html")


def about_page(request):
    return render(request, "core/about_page.html")


def contact_page(request):
    return render(request, "core/contact_page.html")
