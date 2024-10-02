import datetime
import random

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.http import HttpRequest
from django.shortcuts import redirect, render

from . import utils
from .containers import *
from .models import *


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

        else:
            return render(
                request,
                "views/login.html",
                {"message": "Ulanyjy adyňyz ýa-da/we açar sözüňiz nädogry"},
            )
    else:
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return render(
                request,
                "views/login.html",
            )


def register_view(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensuring password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "flight/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(
                request, "flight/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return redirect("home")
    else:
        return render(request, "flight/register.html")


@login_required(login_url="/login/")
def logout_view(request):
    logout(request)
    return redirect("home")


@login_required(login_url="/login/")
def main(request: HttpRequest):
    if request.user.groups.contains(Group.objects.get(name="Moderator")):
        projects_count = Project.objects.all().count()
        rated_projects_count = Project.rated_objects.all().count()
        unrated_projects_count = Project.unrated_objects.all().count()
        return render(
            request,
            "views/main/moderator.html",
            {
                "projects_count": projects_count,
                "rated_projects_count": rated_projects_count,
                "unrated_projects_count": unrated_projects_count,
            },
        )
    return render(request, "views/main/jury.html")


def add_project(request: HttpRequest):
    directions = Direction.objects.all()
    if request.method == "POST":
        if request.POST["personality_type"] == "1":
            personality_type = Project.PersonalityType.INDIVIDUAL
        elif request.POST["personality_type"] == "2":
            personality_type = Project.PersonalityType.LEGAL
        else:
            return render(
                request,
                "views/add_project.html",
                {
                    "directions": directions,
                    "message": "Şahsyýet görnüşini dogry giriziň!",
                },
            )
        try:
            direction = Direction.objects.get(pk=int(request.POST["direction"]))
        except:
            return render(
                request,
                "views/add_project.html",
                {
                    "directions": directions,
                    "message": "Ugry dogry giriziň!",
                },
            )
        try:
            project = Project.objects.create(
                personality_type=personality_type,
                agency=request.POST["agency"],
                direction=direction,
                place_of_residence=request.POST["place_of_residence"],
                full_name_of_manager=request.POST["manager_full_name"],
                phone_number=request.POST["phone_number"],
                additional_phone_number=request.POST["additional_phone_number"],
                email=request.POST["email"],
                description=request.POST["description"],
                p_copy_page1=request.FILES["page1"],
                p_copy_page2_3=request.FILES["page2_3"],
                p_copy_page5_6=request.FILES["page5_6"],
                p_copy_page32=request.FILES["page32"],
            )
            if request.POST.get("second_member_full_name", False):
                if request.POST["second_member_full_name"] != "ýok":
                    project.full_name_of_second_participant = request.POST[
                        "second_member_full_name"
                    ]
            if request.POST.get("third_member_full_name", False):
                if request.POST["third_member_full_name"] != "ýok":
                    project.full_name_of_third_participant = request.POST[
                        "third_member_full_name"
                    ]
            project.save()
        except:
            return render(
                request,
                "views/add_project.html",
                {"message": "Ýalňyşlyk döredi!", "directions": directions},
            )

        print(request.POST)
        print(request.FILES)
    return render(request, "views/add_project.html", {"directions": directions})
