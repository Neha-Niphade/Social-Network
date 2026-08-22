from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.db.models import Q

from .forms import TweetForm
from .models import Comment, Notification, Tweet

from .permissions import IsOwnerOrReadOnly

from .services.moderation import moderate_tweet

def home(request):
    tweets = Tweet.objects.all().order_by("-created_at")

    paginator = Paginator(tweets, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tweets/home.html",
        {
            "page_obj": page_obj,
        },
    )


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

        if tweet.user != request.user:
            Notification.objects.create(
                user=tweet.user,
                message=f"{request.user.username} liked your tweet."
            )

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

        if tweet.user != request.user:
            Notification.objects.create(
                user=tweet.user,
                message=f"{request.user.username} commented on your tweet."
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
    
def tweet_detail(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    return render(
        request,
        "tweets/tweet_detail.html",
        {"tweet": tweet},
    )

@login_required
def tweet_bookmark(request, tweet_id):
    tweet = get_object_or_404(Tweet, id=tweet_id)

    if tweet.bookmarks.filter(id=request.user.id).exists():
        tweet.bookmarks.remove(request.user)
    else:
        tweet.bookmarks.add(request.user)

    return redirect("tweet_list")

@login_required
def saved_tweets(request):
    tweets = request.user.bookmarked_tweets.all()

    return render(
        request,
        "tweets/saved_tweets.html",
        {"tweets": tweets},
    )

def search(request):
    query = request.GET.get("q", "").strip()

    tweets = Tweet.objects.filter(
    Q(text__icontains=query) |
    Q(user__username__icontains=query)
    )

    users = User.objects.filter(
        username__icontains=query
    )

    return render(
        request,
        "tweets/search.html",
        {
            "query": query,
            "tweets": tweets,
            "users": users,
        },
    )

@login_required
def following_feed(request):

    following_users = request.user.profile.following.all()

    tweets = Tweet.objects.filter(
        user__in=following_users
    ).order_by("-created_at")

    paginator = Paginator(tweets, 10)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tweets/following_feed.html",
        {"page_obj": page_obj},
    )

@login_required
def notifications(request):
    notifications = request.user.notifications.all().order_by("-created_at")
    notifications.update(is_read=True)

    return render(
        request,
        "tweets/notifications.html",
        {"notifications": notifications},
    )

from rest_framework import permissions, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import TweetSerializer, CommentSerializer

class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.select_related("user").prefetch_related(
        "likes",
        "bookmarks",
        "comments",
    ).order_by("-created_at")

    serializer_class = TweetSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    parser_classes = [
        JSONParser,
        MultiPartParser,
        FormParser,
    ]

    def perform_create(self, serializer):
        text = serializer.validated_data.get("text", "")

        if not moderate_tweet(text):
            from rest_framework.exceptions import ValidationError

            raise ValidationError(
                {
                    "text": "This tweet was flagged by AI moderation."
                }
            )

        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.select_related(
        "user",
        "tweet",
    ).prefetch_related(
        "likes",
    ).order_by("-created_at")

    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})