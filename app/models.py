from datetime import datetime, timezone
from uuid import uuid4

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


def get_datetime() -> datetime:
    return datetime.now(timezone.utc)


def check_date_created(dt: datetime) -> None:
    if dt > get_datetime():
        raise ValidationError(
            "Date and time is bigger than current!", params={"created": dt}
        )


class CreatedMixin(models.Model):
    created = models.DateTimeField(
        "created",
        default=get_datetime,
        null=True,
        blank=True,
        validators=[check_date_created],
    )

    class Meta:
        abstract = True


class Status(models.TextChoices):
    READY = "готов", "Готов"
    IN_DEVELOPMENT = "в разработке", "В разработке"


class Project(UUIDMixin):
    name = models.TextField("name", null=False, blank=False)
    date_start = models.DateField("date_start", null=False, blank=False)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_DEVELOPMENT,
        verbose_name="Статус",
    )

    class Meta:
        db_table = '"django_hw"."project"'
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self) -> str:
        return f"Project {self.name} with start data: {self.date_start}"


class Developer(UUIDMixin, CreatedMixin):
    name = models.TextField("name", null=False, blank=False)
    surname = models.TextField("surname", null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.TextField("position", null=False, blank=False)

    class Meta:
        db_table = '"django_hw"."developer"'
        verbose_name = "developer"
        verbose_name_plural = "developers"

    def __str__(self):
        return self.name


class Team(UUIDMixin, CreatedMixin):
    name = models.TextField("name", null=False, blank=False)
    developers = models.ManyToManyField(
        "developer", related_name="team_developer"
    )
    projects = models.ManyToManyField(
        "project", related_name="teams", blank=True
    )

    class Meta:
        db_table = '"django_hw"."team"'
        verbose_name = "team"
        verbose_name_plural = "teams"

    def __str__(self) -> str:
        return f"In team {self.name} developers: {self.developers}"
