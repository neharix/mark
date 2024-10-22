import random

from django.conf import settings
from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class RatedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(rated=True)


class UnratedManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super().get_queryset().filter(rated=False)


class Project(models.Model):
    agency = models.CharField(verbose_name="Edara", max_length=200)
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
    direction = models.ForeignKey(
        "Direction", verbose_name="Ugry", on_delete=models.PROTECT
    )
    description = models.TextField(
        verbose_name="Taslamanyň beýany", null=True, blank=True
    )
    rated = models.BooleanField(default=False)

    objects = models.Manager()
    rated_objects = RatedManager()
    unrated_objects = UnratedManager()

    class Meta:
        verbose_name = "taslama"
        verbose_name_plural = "taslamalar"

    def __str__(self) -> str:
        return f"{self.full_name_of_manager} {self.description} taslamasy"


class Direction(models.Model):
    name = models.CharField(verbose_name="Ugur", max_length=100)

    class Meta:
        verbose_name = "ugur"
        verbose_name_plural = "ugurlar"

    def __str__(self) -> str:
        return self.name


class Schedule(models.Model):
    quene_json = models.TextField("Reje JSON-y")
    juries = models.ManyToManyField(User, verbose_name="Emin agzalar")
    date = models.DateField("Senesi")

    class Meta:
        verbose_name = "reje"
        verbose_name_plural = "rejeler"

    def __str__(self):
        return self.date.strftime("%d.%m.%Y")


class Mark(models.Model):
    jury = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    mark = models.IntegerField()
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "baha"
        verbose_name_plural = "bahalar"

    def __str__(self):
        return f"{self.date} {self.project}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Ulanyjy")
    password = models.CharField(max_length=250, verbose_name="Açar sözi")
    active_jury = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} profili"

    class Meta:
        verbose_name = "profil"
        verbose_name_plural = "profiller"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance,
            password="<undefined>",
        )
