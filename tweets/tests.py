from django.test import TestCase
from django.contrib.auth.models import User
from .models import Tweet, Comment, Notification


class TweetTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123"
        )

    # 1. Test tweet creation
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

    # 2. User cannot edit another user's tweet
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

    # 3. Test like and unlike
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
            tweet.likes.filter(
                id=self.user.id
            ).exists()
        )

        # Unlike
        response = self.client.post(
            f"/tweet/{tweet.id}/like/"
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            tweet.likes.filter(
                id=self.user.id
            ).exists()
        )

    # 4. Like creates notification
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

    # 5. Comment creates notification
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

    # 6. User cannot delete another user's tweet
    def test_user_cannot_delete_other_users_tweet(self):
        other_user = User.objects.create_user(
            username="deleteuser",
            password="deletepass123"
        )

        tweet = Tweet.objects.create(
            user=other_user,
            text="This tweet should not be deleted"
        )

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(
            f"/tweet/{tweet.id}/delete/"
        )

        self.assertEqual(response.status_code, 403)

        self.assertTrue(
            Tweet.objects.filter(
                id=tweet.id
            ).exists()
        )

    # 7. User cannot edit another user's comment
    def test_user_cannot_edit_other_users_comment(self):
        other_user = User.objects.create_user(
            username="commentuser",
            password="commentpass123"
        )

        tweet = Tweet.objects.create(
            user=other_user,
            text="Tweet for comment test"
        )

        comment = Comment.objects.create(
            user=other_user,
            tweet=tweet,
            text="Original comment"
        )

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(
            f"/comment/{comment.id}/edit/",
            {
                "text": "Changed comment"
            }
        )

        self.assertEqual(response.status_code, 302)

        comment.refresh_from_db()

        self.assertEqual(
            comment.text,
            "Original comment"
        )

    # 8. User cannot delete another user's comment
    def test_user_cannot_delete_other_users_comment(self):
        other_user = User.objects.create_user(
            username="commentdeleteuser",
            password="commentdeletepass123"
        )

        tweet = Tweet.objects.create(
            user=other_user,
            text="Tweet for delete comment test"
        )

        comment = Comment.objects.create(
            user=other_user,
            tweet=tweet,
            text="Comment that should remain"
        )

        self.client.login(
            username="testuser",
            password="testpass123"
        )

        response = self.client.post(
            f"/comment/{comment.id}/delete/"
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            Comment.objects.filter(
                id=comment.id
            ).exists()
        )

    # 9. Logged-out users cannot create tweets
    def test_logged_out_user_cannot_create_tweet(self):
        response = self.client.get("/create/")

        self.assertEqual(response.status_code, 302)

        self.assertIn(
            "/accounts/login/",
            response.url
        )

    # 10. Logged-out users cannot like a tweet
    def test_logged_out_user_cannot_like_tweet(self):
        tweet = Tweet.objects.create(
            user=self.user,
            text="Tweet for authentication test"
        )

        response = self.client.post(
            f"/tweet/{tweet.id}/like/"
        )

        self.assertEqual(response.status_code, 302)

        self.assertTrue(
            response.url.startswith("/accounts/login/")
        )

        self.assertFalse(
            tweet.likes.exists()
        )