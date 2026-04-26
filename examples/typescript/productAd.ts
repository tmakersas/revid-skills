/**
 * Example: product description -> AI ad video.
 *
 *   REVID_API_KEY=… npx tsx productAd.ts "Your product description…"
 */
import { render, waitFor } from "./revidClient";

async function main(description: string) {
  const payload = {
    workflow: "ad-generator",
    source: {
      prompt: description,
      stylePrompt:
        "Lead with a sharp question hook. Then 2 short benefit beats. " +
        "Close with the price and a single CTA. Tone: confident, calm, premium.",
      durationSeconds: 22,
    },
    aspectRatio: "9:16",
    voice:    { enabled: true, stability: 0.55, speed: 1.05, language: "en-US" },
    captions: { enabled: true, position: "middle", autoCrop: true },
    music:    { enabled: true, syncWith: "beats", trackName: "ad-energetic" },
    media: {
      type: "stock-video",
      density: "high",
      animation: "dynamic",
      quality: "ultra",
      imageModel: "ultra",
      videoModel: "ultra",
      turnImagesIntoVideos: true,
    },
    options: {
      targetDuration: 22,
      promptTargetDuration: 22,
      summarizationPreference: "summarizeIfLong",
      hasToGenerateCover: true,
      coverTextType: "hook",
      addStickers: true,
      soundEffects: true,
    },
    render: { resolution: "1080p", frameRate: 30 },
  };

  const pid = await render(payload);
  console.log("pid=", pid);
  const result = await waitFor(pid);
  console.log("ready:", result.videoUrl);
}

main(
  process.argv[2] ??
    "AeroPods Pro — wireless earbuds with adaptive ANC, 38h battery, IPX5, USB-C wireless charging. $179.",
).catch((e) => {
  console.error(e);
  process.exit(1);
});
