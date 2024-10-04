from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.contrib import messages
from user.forms import *


# Create your views here.
class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = "user/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["title"] = "Profile"
        context["form"] = ProfileForm(instance=self.request.user)
        return context

    def post(self, request, *args, **kwargs):
        form = ProfileForm(
            request.POST, instance=request.user
        )  # Bind the form to the request user
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            messages.error(request, "Form has some errors.")
            return self.render_to_response(self.get_context_data(form=form))


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("user_index")

        form = CreateUserForm()
        return render(request, "user/register.html", {"registerform": form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_mail(
                subject="Welcome to our Shop!",
                message=f"Thank you for registering {user.username}. We are happy to have you!",
                from_email=None,  # Use DEFAULT_FROM_EMAIL instead
                recipient_list=[user.email],  # Send email to the registered user
                fail_silently=False,
            )
            messages.success(
                request,
                "Your account has been created successfully! Now you can login with your credentials.",
            )
            return redirect("login")

        return render(request, "user/register.html", {"registerform": form})


def login(request):
    if request.user.is_authenticated:
        return redirect("user_index")

    form = LoginForm()

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("user_index")

    return render(request, "user/login.html", {"loginform": form})


def logout(request):
    auth.logout(request)
    return redirect("login")
