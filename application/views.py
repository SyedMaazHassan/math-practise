from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.http import JsonResponse
import json

# main page function


def index(request):
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, 'profile.html')


# function for signup

def signup(request):
    if request.method == "POST":
        name = request.POST['name']
        l_name = request.POST['l_name']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        context = {
            "name": name,
            "l_name": l_name,
            "email": email,
            "pass1": pass1,
            "pass2": pass2,
        }
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                print("Email already taken")
                messages.info(request, "Entered email already in use!")
                context['border'] = "register-email"
                context['section'] = "register"
                return render(request, "index.html", context)

            user = User.objects.create_user(
                username=email, first_name=name, password=pass1, last_name=l_name)
            user.save()

            messages.info(
                request, "Your account has been created successfully!")
            return redirect("login")
        else:
            messages.info(request, "Your pasword does not match!")
            context['border'] = "register-password"
            context['section'] = "register"
            return render(request, "index.html", context)

    context = {'section': 'register'}
    return render(request, "index.html", context)


# function for login

def login(request):

    if request.method == "POST":
        email = request.POST['login_email']
        password = request.POST['login_password']
        context = {
            'login_email': email,
            'login_password': password
        }
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            context['section'] = "login"
            messages.info(request, "Incorrect login details!")
            return render(request, "index.html", context)
            # return redirect("login")
    else:
        context = {'section': 'login'}
        return render(request, "index.html", context)


# function for logout

def logout(request):
    auth.logout(request)
    return redirect("index")
