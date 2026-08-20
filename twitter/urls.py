from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    # Main application
    path("", include("tweets.urls")),

    # Authentication
    path("accounts/", include("django.contrib.auth.urls")),

    # Profiles
    path("profile/", include("profiles.urls")),

    # REST API
    path("api/", include("tweets.api_urls")),
]


urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)