from django.contrib import admin
from django.urls import path, include
from tweets import views

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("tweets.urls")),

    path("register/", views.register, name="register"),

    path("accounts/", include("django.contrib.auth.urls")),

    path("profile/", include("profiles.urls")),
]