from django.shortcuts import render, redirect
from .models import Tweet
from .forms import TweetForm


def home(request):
    tweets = Tweet.objects.all()
    return render(request, "tweets/home.html", {"tweets": tweets})


def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("tweet_list")
    else:
        form = TweetForm()

    return render(request, "tweets/tweet_form.html", {"form": form})