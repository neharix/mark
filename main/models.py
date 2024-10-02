from django.contrib.auth.models import AbstractUser
from django.db import models


class RatedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(rated=True)


class UnratedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(rated=False)


class Project(models.Model):
    class PersonalityType(models.TextChoices):
        INDIVIDUAL = "Fiziki", "Fiziki"
        LEGAL = "Ýuridiki", "Ýuridiki"

    personality_type = models.CharField(
        verbose_name="Şahs görnüşi",
        max_length=50,
        choices=PersonalityType.choices,
        default=PersonalityType.INDIVIDUAL,
    )
    agency = models.CharField(verbose_name="Edara", max_length=200)
    place_of_residence = models.CharField(verbose_name="Ýaşaýan ýeri", max_length=200)
    full_name_of_manager = models.CharField(
        verbose_name="Topar ýolbaşçysynyň F.A.Aa", max_length=200
    )
    full_name_of_second_participant = models.CharField(
        verbose_name="Toparyň ikinji agzasyňyň F.A.Aa",
        max_length=200,
        null=True,
        blank=True,
    )
    full_name_of_third_participant = models.CharField(
        verbose_name="Toparyň üçinji agzasyňyň F.A.Aa",
        max_length=200,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(verbose_name="Telefon belgi", max_length=8)
    additional_phone_number = models.CharField(
        verbose_name="Telefon belgi", max_length=8
    )
    email = models.EmailField("Email")
    direction = models.ForeignKey(
        "Direction", verbose_name="Ugry", on_delete=models.PROTECT
    )
    description = models.TextField(
        verbose_name="Taslamanyň beýany", null=True, blank=True
    )
    rated = models.BooleanField(default=False)

    p_copy_page1 = models.ImageField(
        verbose_name="Topar ýolbaşçysynyň pasport nusgasy (sahypa 1)",
        upload_to="passport_copies/1/",
    )
    p_copy_page2_3 = models.ImageField(
        verbose_name="Topar ýolbaşçysynyň pasport nusgasy (sahypa 2-3)",
        upload_to="passport_copies/2-3/",
    )
    p_copy_page5_6 = models.ImageField(
        verbose_name="Topar ýolbaşçysynyň pasport nusgasy (sahypa 5-6)",
        upload_to="passport_copies/5-6/",
    )
    p_copy_page32 = models.ImageField(
        verbose_name="Topar ýolbaşçysynyň pasport nusgasy (sahypa 32)",
        upload_to="passport_copies/32/",
    )

    objects = models.Manager()
    rated_objects = RatedManager()
    unrated_objects = UnratedManager()

    def __str__(self) -> str:
        return f"{self.full_name_of_manager} taslamasy"


class Direction(models.Model):
    name = models.CharField(verbose_name="Ugur", max_length=100)

    def __str__(self) -> str:
        return self.name


class User(AbstractUser):
    pass
