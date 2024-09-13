from django.contrib import admin

from app.models import Developer, Project, Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    class Meta:
        model = Team

    list_display = (
        "name",
    )


@admin.register(Developer)
class DeveloperAdmin(admin.ModelAdmin):
    class Meta:
        model = Developer

    list_display = ("name", "surname", "position")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    class Meta:
        model = Project

    list_display = (
        "name",
        "status",
    )
