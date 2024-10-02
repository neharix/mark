import datetime
import random
import zipfile
from io import BytesIO

import numpy as np
import pandas as pd
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


def add_project_using_xlsx(request: HttpRequest):
    if request.method == "POST":
        dataframe = pd.read_excel(request.FILES.get("xlsx"))
        for index in range(len(dataframe["Ýolbaşçynyň F.A.A"])):
            print("")
            print(dataframe["Şahs"][index])
            print(dataframe["Ýolbaşçynyň F.A.A"][index])
            print(dataframe["Ikinji agzanyň F.A.A"][index])
            print(type(dataframe["Üçünji agzanyň F.A.A"][index]) == np.float64)
            print(dataframe["Edaranyň ady"][index])
            print(dataframe["Ugry"][index])
            print(dataframe["Taslamanyň beýany"][index])
            print(dataframe["Ýolbaşçynyň telefon belgisi"][index])
            print(dataframe["Goşmaça telefon belgisi"][index])
            print(dataframe["Email"][index])
            print(dataframe["Pasportyň 1-nji sahypasy"][index])
            print(dataframe["Pasportyň 2-3-nji sahypalary"][index])
            print(dataframe["Pasportyň 5-6-nji sahypalary"][index])
            print(dataframe["Pasportyň 32-nji sahypasy"][index])

            if dataframe["Şahs"][index].lower() == "fiziki":
                personality_type = Project.PersonalityType.INDIVIDUAL
            elif dataframe["Şahs"][index].lower() == "ýuridiki":
                personality_type = Project.PersonalityType.LEGAL

        zip_file_memory = request.FILES.get("zipfile", None)
        if zip_file_memory is not None:
            zip_file = BytesIO(zip_file_memory.read())
            with zipfile.ZipFile(zip_file, "r") as file:
                images = file.namelist()

    #               question_text[0:2] == "{{"
    #                 and question_text[len(question_text) - 2 : len(question_text)] == "}}"
    #             ):
    #                 filename = question_text.split('"')[1]
    #                 if filename in images:
    #                     is_image = True
    #                     with zipfile.ZipFile(zip_file, "r") as file:
    #                         file.extract(filename, f"temp/{filename}")
    #                     with open(f"temp/{filename}/{filename}", "rb") as file:
    #                         image = file.read()
    #                     os.remove(f"temp/{filename}/{filename}")
    #                     os.rmdir(f"temp/{filename}")

    return render(request, "views/add_project_using_xlsx.html")


# def import_from_xlsx(request: HttpRequest, challenge_id: int):
#     if request.method == "POST":
#         dataframe = pd.read_excel(request.FILES.get("excel"))

#         easy_question_count = 0
#         medium_question_count = 0
#         hard_question_count = 0

#         for index in range(len(dataframe["Sorag"])):
#             if dataframe["Derejesi"][index] == "Ýeňil":
#                 easy_question_count += 1
#             elif dataframe["Derejesi"][index] == "Ortaça":
#                 medium_question_count += 1
#             elif dataframe["Derejesi"][index] == "Kyn":
#                 hard_question_count += 1

#         default_question_count = min(
#             [
#                 easy_question_count if easy_question_count != 0 else 1,
#                 medium_question_count if medium_question_count != 0 else 1,
#                 hard_question_count if hard_question_count != 0 else 1,
#             ]
#         )

#         question_complexity_counts = {
#             "Ýeňil": 0,
#             "Ortaça": 0,
#             "Kyn": 0,
#         }

#         zip_file_memory = request.FILES.get("zip", None)
#         if zip_file_memory is not None:
#             zip_file = BytesIO(zip_file_memory.read())
#             with zipfile.ZipFile(zip_file, "r") as file:
#                 images = file.namelist()
#         challenge = Challenge.objects.get(pk=challenge_id)

#         for index in range(len(dataframe["Sorag"])):
#             is_image = False
#             question_text = str(dataframe["Sorag"][index])
#             if (
#                 question_text[0:2] == "{{"
#                 and question_text[len(question_text) - 2 : len(question_text)] == "}}"
#             ):
#                 filename = question_text.split('"')[1]
#                 if filename in images:
#                     is_image = True
#                     with zipfile.ZipFile(zip_file, "r") as file:
#                         file.extract(filename, f"temp/{filename}")
#                     with open(f"temp/{filename}/{filename}", "rb") as file:
#                         image = file.read()
#                     os.remove(f"temp/{filename}/{filename}")
#                     os.rmdir(f"temp/{filename}")

#             complexity = Complexity.objects.get(level=dataframe["Derejesi"][index])
#             if question_complexity_counts[complexity.level] < default_question_count:
#                 question_complexity_counts[complexity.level] += 1
#                 question = (
#                     Question.objects.create(
#                         question=question_text,
#                         challenge=challenge,
#                         point=1,
#                         complexity=complexity,
#                     )
#                     if is_image == False
#                     else Question.objects.create(
#                         challenge=challenge,
#                         point=1,
#                         complexity=complexity,
#                         is_image=is_image,
#                         image=ContentFile(image, filename),
#                     )
#                 )
#                 true_answer = (
#                     dataframe["Dogry jogap"][index]
#                     if type(dataframe["Dogry jogap"][index]) == int
#                     else int(dataframe["Dogry jogap"][index])
#                 )
#                 for i in range(1, 5):
#                     if type(dataframe[f"{i}-nji jogap"][index]) != float:
#                         is_image = False
#                         answer_text = str(dataframe[f"{i}-nji jogap"][index])
#                         if (
#                             answer_text[0:2] == "{{"
#                             and answer_text[len(answer_text) - 2 : len(answer_text)]
#                             == "}}"
#                         ):
#                             filename = answer_text.split('"')[1]
#                             if filename in images:
#                                 is_image = True
#                                 with zipfile.ZipFile(zip_file, "r") as file:
#                                     file.extract(filename, f"temp/{filename}")
#                                 with open(f"temp/{filename}/{filename}", "rb") as file:
#                                     image = file.read()
#                                 os.remove(f"temp/{filename}/{filename}")
#                                 os.rmdir(f"temp/{filename}")
#                         if is_image:
#                             answer = (
#                                 Answer.objects.create(
#                                     image=ContentFile(image, filename),
#                                     question=question,
#                                     is_true=True,
#                                     is_image=is_image,
#                                 )
#                                 if true_answer == i
#                                 else Answer.objects.create(
#                                     image=ContentFile(image, filename),
#                                     question=question,
#                                     is_image=is_image,
#                                 )
#                             )
#                         else:
#                             answer = (
#                                 Answer.objects.create(
#                                     answer=answer_text, question=question, is_true=True
#                                 )
#                                 if true_answer == i
#                                 else Answer.objects.create(
#                                     answer=answer_text, question=question
#                                 )
#                             )
#             else:
#                 continue

#         return render(
#             request,
#             "import_from_xlsx.html",
#             {"type": "success", "message": "Maglumat gorunda üstünlikli girizildi!"},
#         )
#     return render(request, "import_from_xlsx.html")
