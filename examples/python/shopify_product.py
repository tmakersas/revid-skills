"""
Example: Shopify product URL -> 9:16 promo video.

Usage:
    REVID_API_KEY=… python shopify_product.py https://your-shop.com/products/x
"""
import sys

from revid_client import render, wait_for


def main(url: str) -> None:
    payload = {
        "workflow": "article-to-video",
        "source": {
            "url": url,
            "scrapingPrompt": (
                "Extract the product name, hero image, 3 key features, and price. "
                "Ignore reviews, related products, footer, and navigation."
            ),
        },
        "aspectRatio": "9:16",
        "voice":    {"enabled": True, "stability": 0.55, "speed": 1.05, "language": "en-US"},
        "captions": {"enabled": True, "position": "middle", "autoCrop": True},
        "music":    {"enabled": True, "syncWith": "beats", "trackName": "uplifting-pop"},
        "media": {
            "type": "stock-video",
            "density": "high",
            "animation": "dynamic",
            "quality": "pro",
            "imageModel": "good",
            "videoModel": "pro",
            "turnImagesIntoVideos": True,
        },
        "options": {
            "targetDuration": 35,
            "summarizationPreference": "summarize",
            "hasToGenerateCover": True,
            "coverTextType": "product-name",
            "soundEffects": True,
        },
        "render": {"resolution": "1080p", "frameRate": 30},
    }

    pid = render(payload)
    print(f"pid={pid}")
    result = wait_for(pid)
    print("ready:", result.get("videoUrl"))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "https://soundlabs.shop/products/aeropods-pro")
