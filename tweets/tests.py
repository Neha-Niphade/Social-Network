from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tweet, Notification


class TweetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    def test_user_can_create_tweet(self):
        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(
            "/create/",
            {
                "text": "Hello from a test!"
            }
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Tweet.objects.filter(
                text="Hello from a test!",
                user=self.user
            ).exists()
        )

def test_user_cannot_edit_other_users_tweet(self):
    other_user = User.objects.create_user(
        username="otheruser",
        password="otherpass123"
    )

    tweet = Tweet.objects.create(
        user=other_user,
        text="Other user's tweet"
    )

    self.client.login(
        username="testuser",
        password="testpass123"
    )

    response = self.client.post(
        f"/tweet/{tweet.id}/edit/",
        {
            "text": "I changed your tweet!"
        }
    )

    self.assertEqual(response.status_code, 403)

    tweet.refresh_from_db()

    self.assertEqual(
        tweet.text,
        "Other user's tweet"

    )

def test_user_can_like_and_unlike_tweet(self):
    tweet = Tweet.objects.create(
        user=self.user,
        text="Tweet for testing likes"
    )

    self.client.login(
        username="testuser",
        password="testpass123"
    )

    # Like
    response = self.client.post(
        f"/tweet/{tweet.id}/like/"
    )

    self.assertEqual(response.status_code, 302)
    self.assertTrue(
        tweet.likes.filter(id=self.user.id).exists()
    )

    # Unlike
    response = self.client.post(
        f"/tweet/{tweet.id}/like/"
    )

    self.assertEqual(response.status_code, 302)
    self.assertFalse(
        tweet.likes.filter(id=self.user.id).exists()
    )

def test_like_creates_notification(self):
    other_user = User.objects.create_user(
        username="otheruser",
        password="otherpass123"
    )

    tweet = Tweet.objects.create(
        user=other_user,
        text="Tweet for notification test"
    )

    self.client.login(
        username="testuser",
        password="testpass123"
    )

    self.client.post(
        f"/tweet/{tweet.id}/like/"
    )

    notification = Notification.objects.filter(
        user=other_user
    ).first()

    self.assertIsNotNone(notification)

    self.assertEqual(
        notification.message,
        "testuser liked your tweet."
    )

def test_comment_creates_notification(self):
    other_user = User.objects.create_user(
        username="otheruser",
        password="otherpass123"
    )

    tweet = Tweet.objects.create(
        user=other_user,
        text="Tweet for comment notification"
    )

    self.client.login(
        username="testuser",
        password="testpass123"
    )

    response = self.client.post(
        f"/tweet/{tweet.id}/comment/",
        {
            "text": "Nice tweet!"
        }
    )

    self.assertEqual(response.status_code, 302)

    notification = Notification.objects.filter(
        user=other_user
    ).first()

    self.assertIsNotNone(notification)

    self.assertEqual(
        notification.message,
        "testuser commented on your tweet."
    )