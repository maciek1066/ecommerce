from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User


# basic view with links to login/register
class BasicView(View):
    def get(self, request):
        return render(
            request,
            template_name="main.html",
            context={}
        )


# registration
class AddUserView(View):
    def get(self, request):
        form = AddUserForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='register.html',
            context=ctx
        )

    def post(self, request):
        form = AddUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if User.objects.filter(username=username).exists():
                form.add_error('username', "username already exists")
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            if password != password2:
                form.add_error('password', "Passwords don't match")
            if not form.errors:
                User.objects.create_user(
                    username=username,
                    password=password
                )
                return redirect("/login")
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='register.html',
            context=ctx
        )


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='login.html',
            context=ctx
        )

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in")
                return redirect("/lobby")
            return HttpResponse("Try again")
        ctx = {
            'form': form
        }
        return render(
            request,
            template_name='login.html',
            context=ctx
        )


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/login")

