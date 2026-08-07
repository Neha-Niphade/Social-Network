from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from tweets.models import Tweet

def profile_detail(request, username):
    user = get_object_or_404(User, username=username)

    profile = user.profile

    tweets = Tweet.objects.filter(user=user).order_by("-created_at")

    context = {
        "profile": profile,
        "tweets": tweets,
    }

    return render(request, "profiles/profile_detail.html", context)