from django.contrib import admin
from django.urls import path, include
from tweets import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", include("tweets.urls")),

    path("register/", views.register, name="register"),

    path("accounts/", include("django.contrib.auth.urls")),

    path("profile/", include("profiles.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)