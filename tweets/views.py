from django.shortcuts import render, redirect
from .models import Tweet
from .forms import TweetForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Tweet, Comment

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

@login_required
def tweet_edit(request, tweet_id):
    # Fetch the tweet from the database
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    # Authorization: Only the owner can edit
    if tweet.user != request.user:
        raise PermissionDenied

    # If the user submits the form
    if request.method == "POST":
        form = TweetForm(request.POST, request.FILES, instance=tweet)

        if form.is_valid():
            form.save()
            return redirect("tweet_list")

    # If the user just opens the page
    else:
        form = TweetForm(instance=tweet)

    return render(request, "tweets/tweet_form.html", {"form": form})

@login_required
def tweet_delete(request, tweet_id):
    # Step 1: Fetch the tweet
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    # Step 2: Check ownership
    if tweet.user != request.user:
        raise PermissionDenied

    # Step 3: Delete only after confirmation
    if request.method == "POST":
        tweet.delete()
        return redirect("tweet_list")

    # Step 4: Show confirmation page
    return render(
        request,
        "tweets/tweet_confirm_delete.html",
        {"tweet": tweet},
    )
    
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

@login_required
def tweet_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)

    return redirect("tweet_list")

@login_required
def comment_create(request, tweet_id):
    if request.method != "POST":
        return redirect("tweet_list")

    tweet = get_object_or_404(Tweet, id=tweet_id)

    text = request.POST.get("text", "").strip()

    if text:
        Comment.objects.create(
            user=request.user,
            tweet=tweet,
            text=text,
        )

    return redirect("tweet_list")

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return redirect("tweet_list")

    if request.method == "POST":
        comment.delete()

    return redirect("tweet_list")

@login_required
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if comment.user != request.user:
        return redirect("tweet_list")

    if request.method == "POST":
        text = request.POST.get("text", "").strip()

        if text:
            comment.text = text
            comment.save()

            return redirect("tweet_list")

    return render(
        request,
        "tweets/comment_edit.html",
        {"comment": comment},
    )
    
@login_required
def comment_like(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == "POST":
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)

    return redirect("tweet_list")