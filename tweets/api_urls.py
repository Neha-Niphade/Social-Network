from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TweetViewSet, CommentViewSet


router = DefaultRouter()

router.register("tweets", TweetViewSet, basename="api-tweet")
router.register("comments", CommentViewSet, basename="api-comment")


urlpatterns = [
    path("", include(router.urls)),
]