"""
Example: daily news short on a topic. Schedule with cron / GitHub Actions.

Usage:
    REVID_API_KEY=… python news_daily.py "AI coding tools released this week"
"""
import sys
from datetime import date

from revid_client import render, wait_for


def main(topic: str) -> None:
    payload = {
        "workflow": "article-to-video",
        "source": {
            "prompt": f"{topic} — week of {date.today().isoformat()}",
        },
        "aspectRatio": "9:16",
        "voice":    {"enabled": True, "stability": 0.6, "speed": 1.0},
        "captions": {"enabled": True, "position": "middle", "autoCrop": True},
        "music":    {"enabled": True, "syncWith": "beats"},
        "media": {
            "type": "stock-video",
            "density": "medium",
            "animation": "soft",
            "quality": "pro",
            "videoModel": "pro",
        },
        "options": {
            "fetchNews": True,
            "targetDuration": 45,
            "summarizationPreference": "summarize",
            "hasToGenerateCover": True,
            "coverTextType": "headline",
        },
        "render": {"resolution": "1080p"},
    }

    pid = render(payload)
    print(f"pid={pid}")
    print("ready:", wait_for(pid).get("videoUrl"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "AI coding tools released this week")
