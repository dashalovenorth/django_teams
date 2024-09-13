from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.views.generic.base import TemplateView
from rest_framework.authentication import (
    SessionAuthentication,
    TokenAuthentication,
)
from rest_framework.authtoken.models import Token
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.viewsets import ModelViewSet

from app.models import Developer, Project, Team
from app.serializers import (
    DeveloperSerializer,
    ProjectSerializer,
    TeamSerializer,
)

from .forms import ProjectForm, TeamForm


class MyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_superuser)


def create_viewset(model, serializer):
    class CustomViewSet(ModelViewSet):
        queryset = model.objects.all()
        serializer_class = serializer
        permission_classes = [MyPermission]
        authentication_classes = [TokenAuthentication, SessionAuthentication]

    return CustomViewSet


ProjectViewSet = create_viewset(Project, ProjectSerializer)
DeveloperViewSet = create_viewset(Developer, DeveloperSerializer)
TeamViewSet = create_viewset(Team, TeamSerializer)


class HomePage(TemplateView):
    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)
        context["teams"] = Team.objects.all().prefetch_related("projects", "developers")
        context["serializer"] = TeamSerializer
        if self.request.user.is_authenticated:
            context["token"] = Token.objects.get(user=self.request.user)
        return context


class CreateTeamView(CreateView):
    model = Team
    form_class = TeamForm
    template_name = "team_form.html"
    success_url = "/"

    def form_valid(self, form):
        response = super().form_valid(form)
        form.instance.created_by = self.request.user
        return response


class CreateProjectView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "create_project.html"
    success_url = "/"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teams"] = Team.objects.filter(developers__user=self.request.user)
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.save()
        form.save_m2m()
        return super().form_valid(form)


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        name = request.POST["name"]
        surname = request.POST["surname"]

        user = User.objects.create_user(username=username, password=password)

        Token.objects.create(user=user)

        Developer.objects.create(
            user=user, name=name, surname=surname, position="Разработчик"
        )

        login(request, user)

        return redirect("/")

    return render(request, "register.html")
