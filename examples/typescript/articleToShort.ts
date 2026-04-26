/**
 * Example: article URL -> 9:16 short.
 *
 * Run with:
 *   REVID_API_KEY=… npx tsx articleToShort.ts <article-url>
 */
import { render, waitFor } from "./revidClient";

async function main(url: string) {
  const payload = {
    workflow: "article-to-video",
    source: {
      url,
      scrapingPrompt:
        "Summarize the article body. Skip ads, related links, navigation, and footer.",
    },
    aspectRatio: "9:16",
    voice:    { enabled: true, stability: 0.6, speed: 1.0, language: "en-US" },
    captions: { enabled: true, position: "middle", autoCrop: true },
    music:    { enabled: true, syncWith: "beats" },
    media: {
      type: "stock-video",
      density: "medium",
      animation: "soft",
      quality: "pro",
      videoModel: "pro",
      imageModel: "good",
    },
    options: {
      targetDuration: 45,
      summarizationPreference: "summarize",
      hasToGenerateCover: true,
      coverTextType: "headline",
    },
    render: { resolution: "1080p", frameRate: 30 },
  };

  const pid = await render(payload);
  console.log("pid=", pid);
  const result = await waitFor(pid);
  console.log("ready:", result.videoUrl);
}

main(process.argv[2] ?? "https://techreview.io/ai-tools-2026").catch((e) => {
  console.error(e);
  process.exit(1);
});
