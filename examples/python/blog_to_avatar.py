"""
Example: Blog post URL + avatar image -> talking-head video.

Usage:
    REVID_API_KEY=… python blog_to_avatar.py <blog-url> <avatar-image-url>
"""
import sys

from revid_client import render, wait_for


def main(blog_url: str, avatar_url: str) -> None:
    payload = {
        "workflow": "avatar-to-video",
        "source": {
            "url": blog_url,
            "scrapingPrompt": (
                "Extract the article body. Skip header, navigation, "
                "related posts, and footer."
            ),
        },
        "aspectRatio": "9:16",
        "avatar": {
            "enabled": True,
            "url": avatar_url,
            "removeBackground": True,
            "imageModel": "good",
        },
        "voice": {
            "enabled": True,
            "voiceId": "aria-en-us",
            "stability": 0.65,
            "speed": 1.0,
            "language": "en-US",
            "enhanceAudio": True,
        },
        "captions": {"enabled": True, "position": "bottom", "autoCrop": True},
        "music":    {"enabled": False},
        "media": {
            "type": "moving-image",
            "density": "low",
            "animation": "soft",
            "placeAvatarInContext": True,
        },
        "options": {
            "targetDuration": 60,
            "summarizationPreference": "summarize",
            "hasToGenerateCover": True,
        },
        "render": {"resolution": "1080p", "frameRate": 30},
    }

    pid = render(payload)
    print(f"pid={pid}")
    result = wait_for(pid)
    print("ready:", result.get("videoUrl"))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: blog_to_avatar.py <blog-url> <avatar-image-url>", file=sys.stderr)
        sys.exit(2)
    main(sys.argv[1], sys.argv[2])
