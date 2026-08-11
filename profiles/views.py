from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect

from .models import Profile
from tweets.models import Tweet,Notification


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
        # Already following → unfollow
        profile.following.remove(target_user)

    else:
        # Not following → follow
        profile.following.add(target_user)

        # Don't notify when following yourself
        if target_user != request.user:
            Notification.objects.create(
                user=target_user,
                message=f"{request.user.username} started following you."
            )

    return redirect("profile_detail", username=username)
@login_required
def connections(request, username, connection_type):
    user = get_object_or_404(User, username=username)

    if connection_type == "followers":
        users = User.objects.filter(
            profile__in=user.followers.all()
        )
        title = "Followers"

    elif connection_type == "following":
        users = user.profile.following.all()
        title = "Following"

    else:
        return redirect("profile_detail", username=username)

    return render(
        request,
        "profiles/connections.html",
        {
            "users": users,
            "title": title,
            "profile_user": user,
        },
    )