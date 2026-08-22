import os

from google import genai


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def moderate_tweet(text):
    prompt = f"""
You are a content moderation system.

Analyze the following tweet and determine whether it should be
allowed on a general social networking platform.

Tweet:
{text}

Return ONLY one of these two words:

SAFE
FLAGGED

Flag content that contains things such as:
- serious threats
- extreme harassment
- hateful attacks
- explicit violent intent
- clearly dangerous content

Normal opinions, criticism, jokes, disagreement, and casual
conversation should be considered SAFE.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
    )

    result = response.text.strip().upper()

    return result == "SAFE"