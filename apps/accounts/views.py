from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import RegisterForm, LoginForm, UpdateProfileForm


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)

        if form.is_valid():
            user = form.save()

            login(request, user)

            messages.success(
                request,
                "Registration successful. Welcome!"
            )

            return redirect("dashboard:home")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )

def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard:home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome back {user.first_name}!"
            )

            return redirect("dashboard:home")

        else:

            messages.error(
                request,
                "Invalid username or password."
            )

    return render(
        request,
        "accounts/login.html"
    )
    

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("accounts:login")

@login_required
def profile_view(request):
    return render(
        request,
        "accounts/profile.html",
        {
            "user": request.user
        }
    )
    
    
@login_required
def edit_profile(request):

    if request.method == "POST":

        form = UpdateProfileForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            messages.success(
                request,
                "Profile updated successfully."
            )

            return redirect("accounts:profile")

    else:

        form = UpdateProfileForm(instance=request.user)

    return render(
        request,
        "accounts/edit_profile.html",
        {
            "form":form
        }
    )
    
def forgot_password_view(request):
    return render(
        request,
        "accounts/forgot_password.html"
    )    