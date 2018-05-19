from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import LoginForm


def home_page(request):
    if request.method == "GET":
        ctx = {}
    return render(request, "home_page.html", ctx)



def login_page(request):
    form = LoginForm(request.POST or None)
    ctx = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        ctx['form'] = LoginForm()
    return render(request, "auth/login.html", ctx