from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect,render
from tweets.models import Tweet
from .models import Profile

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)

    profile = user.profile

    tweets = Tweet.objects.filter(user=user).order_by("-created_at")

    context = {
        "profile": profile,
        "tweets": tweets,
    }

    return render(request, "profiles/profile_detail.html", context)

@login_required
def follow_user(request, username):
    target_user = get_object_or_404(User, username=username)
    profile = request.user.profile

    if profile.following.filter(id=target_user.id).exists():
        profile.following.remove(target_user)
    else:
        profile.following.add(target_user)

    return redirect("profile_detail", username=username)