from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .models import Profile
from tweets.models import Tweet


def profile_detail(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    following_count = profile.following.count()
    followers_count = user.followers.count()
    tweets = Tweet.objects.filter(user=user)

    is_following = False

    if request.user.is_authenticated:
        is_following = request.user.profile.following.filter(
            id=user.id
        ).exists()

    return render(
        request,
        "profiles/profile_detail.html",
        {
            "profile": profile,
            "tweets": tweets,
            "is_following": is_following,
            "is_following": is_following,
            "following_count": following_count,
            "followers_count": followers_count,
        },
    )


@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = request.user.profile

    if profile.following.filter(id=target_user.id).exists():
        profile.following.remove(target_user)
    else:
        profile.following.add(target_user)

    return redirect("profile_detail", username=username)