from django.urls import path
from . import views

urlpatterns = [
    path("<str:username>/", views.profile_detail, name="profile_detail"),
    path(
    "profile/<str:username>/follow/",
    views.follow_user,
    name="follow_user",
    ),
    path(
    "<str:username>/connections/<str:connection_type>/",
    views.connections,
    name="connections",
    ),
]

