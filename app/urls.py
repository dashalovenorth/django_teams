from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from app import views

router = DefaultRouter()
router.register(r"project", views.ProjectViewSet, basename="project")
router.register(r"developer", views.DeveloperViewSet, basename="developer")
router.register(r"team", views.TeamViewSet, basename="team")

app_name = "team"
urlpatterns = [
    path("api/", include(router.urls)),
    path("", views.HomePage.as_view(), name="home"),
    path("teams/create/", views.CreateTeamView.as_view(), name="create_team"),
    path(
        "projects/create/",
        views.CreateProjectView.as_view(),
        name="create_project",
    ),
    path("register/", views.register, name="register"),
    path("login/", LoginView.as_view(template_name="login.html")),
    path(
        "logout/",
        LogoutView.as_view(next_page="/"),
        name="logout",
    ),
]
