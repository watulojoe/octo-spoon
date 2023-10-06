from django.db import IntegrityError
from django.shortcuts import redirect, render

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from ccc import settings
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from django.template.loader import render_to_string


# Create your views here.
def home_view(request):
    return render(request, "home.html")


def signup_user(request):
    """
    form will have username email and password1 and password2
    after submitting an email will be sent to validate the email
    once you activate your account, you'll be logged out and required to login again
    errors that may occur
    -existing username(unique)
    -existing email(unique)
    -weak password
    -email to validate has not been sent successfully
    """
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        # errors before signup
        if User.objects.filter(email=email):
            return render(request, "auth/signup.html", {"error": "The email is already in use"})
        if len(username) < 2 or len(username) > 10:
            return render(request, "auth/signup.html", {"error": "your username should be 2-10 characters"})
        # todo: username should not be numbers only
        # todo: check if the password entered is strong

        if password1 == password2:
            try:
                new_user = User.objects.create_user(username=username, email=email, password=password1)
                new_user.is_active = False
                new_user.save()

                # confirm email
                # todo: write a funtion to seperate this
                # todo: (waiting_confirmation.html) redirect to confirmemail.html (tells the user to chek their email to activate their acc)
                current_site = get_current_site(request)
                email_subject = "confirm your email"
                message = render_to_string(
                    "auth/email_confirmation.html",
                    {
                        "name": new_user.username,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(new_user.pk)),
                        "token": generate_token.make_token(new_user)
                    }
                )
                email = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [new_user.email])
                email.fail = True
                email.send()
                return render(request, "auth/check_email.html")


            except IntegrityError:
                return render(request, "auth/signup.html",
                              {"error": 'That username has already been taken. Please choose a new username'})
        else:
            return render(request, "auth/signup.html", {"error": "Passwords did not match"})
    else:
        return render(request, "auth/signup.html")


# activate function
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, "auth/activation_failed.html")


# done
def login_user(request):
    """
    using the inbuilt login and authenticate function:
    user will login with his username and password
    after that, directed to home or the page he wanted to access
    errors that may occur
    -wrong email or password
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password1")
        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "auth/login.html", {'error': 'username and password did not match'})
    else:
        return render(request, "auth/login.html")


# done
def logout_user(request):
    """
    using the inbuilt logout funtion
    some browsers open all links found in a website
    logout request method is set to post to avoid being logged out automatically
    """
    if request.method == 'POST':
        logout(request)
        return redirect('home')
