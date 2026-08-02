from django.shortcuts import render, redirect
from .models import Tweet
from .forms import TweetForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


def home(request):
    tweets = Tweet.objects.all()
    return render(request, "tweets/home.html", {"tweets": tweets})


@login_required
def tweet_create(request):
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES)

        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect("tweet_list")

    else:
        form = TweetForm()

    return render(request, "tweets/tweet_form.html", {"form": form})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )