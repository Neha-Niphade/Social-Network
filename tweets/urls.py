from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="tweet_list"),

    path("create/", views.tweet_create, name="tweet_create"),

    path(
        "tweet/<int:tweet_id>/edit/",
        views.tweet_edit,
        name="tweet_edit",
    ),

    path(
        "tweet/<int:tweet_id>/delete/",
        views.tweet_delete,
        name="tweet_delete",
    ),
    path(
        "tweet/<int:tweet_id>/like/",
         views.tweet_like,
         name="tweet_like",
    ),
]