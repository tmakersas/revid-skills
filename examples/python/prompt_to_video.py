"""
Example: One-line idea -> video.

Usage:
    REVID_API_KEY=… python prompt_to_video.py "Why honey never spoils."
"""
import sys

from revid_client import render, wait_for


def main(prompt: str) -> None:
    payload = {
        "workflow": "prompt-to-video",
        "source": {
            "prompt": prompt,
            "stylePrompt": (
                "Open with a punchy hook. End with a takeaway. "
                "Tone: curious, plainspoken."
            ),
            "durationSeconds": 35,
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
            "promptTargetDuration": 35,
            "summarizationPreference": "summarizeIfLong",
            "hasToGenerateCover": True,
        },
        "render": {"resolution": "1080p"},
    }

    pid = render(payload)
    print(f"pid={pid}")
    print("ready:", wait_for(pid).get("videoUrl"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "Why honey never spoils.")
