from django.contrib.auth.models import AbstractUser, User
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


class Criteria(models.Model):
    expression = models.CharField("Kriteriýa aňlatmalary", max_length=400)
    max_value = models.IntegerField("Göterimi")

    class Meta:
        verbose_name = "kriteriýa"
        verbose_name_plural = "kriteriýalar"

    def __str__(self):
        return self.expression


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
    criteria = models.ForeignKey("Criteria", on_delete=models.SET_NULL, null=True)
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
    password = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.user.username} profile"
