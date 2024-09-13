"""Module for urls."""
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    path("token/", views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls')),

]

urlpatterns += staticfiles_urlpatterns()
