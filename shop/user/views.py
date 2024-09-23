from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.contrib.auth import authenticate
from django.contrib.auth.models import auth
from django.contrib.auth.decorators import login_required
from user.forms import CreateUserForm, LoginForm


# Create your views here.
@login_required
def user_index(request):
    print(request.user.is_authenticated)
    t = render_to_string("user/index.html")
    return HttpResponse(t)


@login_required
def user_info(request, id):
    if id > 99:
        raise Http404()
    if id == 0:
        return redirect("/user/")

    return HttpResponse(render_to_string("user/user.html", {"id": id}))


def register(request):
    if request.user.is_authenticated:
        return redirect("user_index")

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
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
