# 02 · API reference

Source: [Revid Public API v3 OpenAPI spec](https://www.revid.ai/postman/revid-public-v3-render.openapi.json)
(`Revid Public API v3 - Simplified Render` · v3.6.0).

## Base URL

```
https://www.revid.ai
```

## Auth

API key, sent as a header named **`key`**:

```
key: $REVID_API_KEY
```

(Not `Authorization: Bearer …`. Header name is literally `key`.)

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `GET`  | `/api/public/v3/render` | Live, machine-readable field reference |
| `POST` | `/api/public/v3/render` | Kick off a render (returns a `pid`) |
| `GET`  | `/api/public/v3/status?pid={pid}` | Poll a render |
| `POST` | `/api/public/v3/calculate-credits` | Estimate cost without rendering |
| `GET`  | `/api/public/v3/projects?limit=10` | List recent projects |
| `POST` | `/api/public/v3/add-to-queue` | Queue an existing project |
| `POST` | `/api/public/v3/publish-now` | Publish to connected social accounts |
| `POST` | `/api/public/v3/export-video` | Re-export an existing project |
| `POST` | `/api/public/v3/rename-project` | Rename a project |
| `GET/POST/DELETE` | `/api/public/v3/consistent-characters` | Manage avatar characters |
| `POST` | `/api/public/v3/buy-credit-pack` | Top up credits |
| `POST` | `/api/public/v3/voice-clone` | Clone a voice from audio |

## `POST /api/public/v3/render`

The single render endpoint takes one request body and dispatches based on
`workflow`. Every skill in this library calls this endpoint.

### Top-level body

```ts
{
  workflow: Workflow,                 // REQUIRED — discriminator (see below)
  source:   SourceInput,              // input content (URL, text, prompt, …)
  aspectRatio?: "9:16" | "1:1" | "16:9" | "portrait" | "landscape" | "square" | "auto",

  webhookUrl?: string,                // POSTed when the render finishes
  projectId?:  string,                // overwrite an existing project

  media?:    MediaConfig,             // visuals
  voice?:    VoiceConfig,             // narration
  captions?: CaptionsConfig,
  music?:    MusicConfig,             // (also accepts `audio` as legacy alias)
  avatar?:   AvatarConfig,
  options?:  OptionsConfig,
  render?:   RenderConfig,            // resolution / fps / compression
  characterIds?: string[],            // referenced consistent characters
  advanced?: { customCreationParams?: object },
  metadata?: object                   // forwarded to creationParams
}
```

### `workflow` enum

| Value | Best for |
|---|---|
| `script-to-video` | You already have the words (a script). |
| `prompt-to-video` | One-line idea — the API writes the script. |
| `article-to-video` | Any URL with text content (blog, product page, news). |
| `avatar-to-video` | Talking-head video from a script + an avatar image. |
| `ad-generator` | Product ad from a description (the AI writes hooks). |
| `music-to-video` | Music clip + visuals. |
| `motion-transfer` | Animate a reference photo with motion from a clip. |
| `caption-video` | Add captions to an existing video. |
| `static-background-video` | Voice over a fixed background asset. |

### `SourceInput`

```ts
{
  text?: string,            // script-to-video: the script
  prompt?: string,          // prompt-to-video, ad-generator: the idea
  stylePrompt?: string,     // optional style instructions
  durationSeconds?: number, // hint for prompt workflows
  url?: string,             // article-to-video, music-to-video, caption-video
  scrapingPrompt?: string,  // custom instructions when scraping `url`
  recordingType?: "video" | "audio",
  websiteToRecord?: string,
  quizzData?: object        // quiz workflow only
}
```

### `MediaConfig`

```ts
{
  type?: "moving-image" | "ai-video" | "video" | "stock-video" | "custom",
  density?: "low" | "medium" | "high",     // # of cuts
  maxItems?: number,                        // hard cap
  animation?: "none" | "soft" | "dynamic" | "depth",
  quality?: "standard" | "pro" | "ultra",
  imageModel?: "cheap" | "good" | "ultra",
  videoModel?: "base" | "pro" | "ultra" | "veo3" | "sora2",
  bRollType?: string,                       // e.g. "split-screen", "fullscreen"
  useOnlyProvided?: boolean,                // ignore stock; use `provided` only
  provided?: MediaItem[],
  backgroundVideo?: MediaItem,
  mergeVideos?: boolean,
  mergeVideosFull?: boolean,
  addAudioToVideos?: boolean,
  turnImagesIntoVideos?: boolean,
  applyStyleTransfer?: boolean,
  placeAvatarInContext?: boolean,
  mediaPreset?: string
}

type MediaItem = {
  url: string,                              // REQUIRED
  type?: "image" | "video" | "audio",
  title?: string,
  urlLowRes?: string,
  imagePreview?: string,
  noReencode?: boolean
}
```

### `VoiceConfig`

```ts
{
  enabled?: boolean,
  voiceId?: string,
  stability?: number,           // 0..1
  speed?: number,               // ~0.7..1.3
  language?: string,            // e.g. "en-US"
  enhanceAudio?: boolean,
  useLegacyModel?: boolean
}
```

### `CaptionsConfig`

```ts
{
  enabled?: boolean,
  preset?: string,                              // brand caption preset id
  position?: "top" | "middle" | "bottom",
  autoCrop?: boolean
}
```

### `MusicConfig`

```ts
{
  enabled?: boolean,
  trackName?: string,
  audioUrl?: string,
  url?: string,
  soundWave?: boolean,
  syncWith?: "beats" | "lyrics",
  generateMusic?: boolean,                      // AI-generate music
  generationMusicPrompt?: string,
  musicGenerationModel?: string,
  enableLyricsLipSync?: boolean,
  generateLyricsFromPrompt?: boolean
}
```

### `AvatarConfig`

```ts
{
  enabled?: boolean,
  url?: string,                                 // avatar image URL
  mimeType?: string,
  imageModel?: string,
  removeBackground?: boolean
}
```

### `OptionsConfig`

```ts
{
  promptTargetDuration?: number,
  targetDuration?: number,
  summarizationPreference?: "summarize" | "summarizeIfLong" | "no-summarization",
  outputCount?: number,
  disableAudio?: boolean,
  disableVoice?: boolean,
  nsfwFilter?: boolean,
  addStickers?: boolean,
  soundEffects?: boolean,
  hasToTranscript?: boolean,
  optimizedForChinese?: boolean,
  language?: string,
  watermark?: object | null,
  useOnlyProvidedMedia?: boolean,
  selectedCharacters?: string[],
  useWholeAudio?: boolean,
  selectedPalette?: string,
  makeLastSlideFillRecordingLength?: boolean,
  preventSummarization?: boolean,
  hasToGenerateCover?: boolean,
  coverTextType?: string,
  fetchNews?: boolean,                          // article workflow: fetch news for topic
  hasTextSmallAtBottom?: boolean,
  customImageGenerationRulesSlug?: string
}
```

### `RenderConfig`

```ts
{
  resolution?: "720p" | "1080p" | "4k",
  compression?: number,                          // 0..100
  frameRate?: number                             // e.g. 24, 30, 60
}
```

### `AdvancedConfig`

```ts
{
  customCreationParams?: object   // expert-mode passthrough; matches legacy
                                  // creationParams shape from the studio
}
```

## Responses

### Success

```json
{
  "success": 1,
  "pid": "p_…",
  "workflow": "article-to-video",
  "webhookUrl": "https://your.webhook/…",
  "endpoint": "/api/public/v3/render",
  "docs": { … }
}
```

### Error

```json
{
  "success": 0,
  "error": "human-readable message",
  "docs": { … }
}
```

## See also

- [03-polling-and-webhooks.md](03-polling-and-webhooks.md) — wait for completion.
- [04-credits-and-pricing.md](04-credits-and-pricing.md) — estimate cost before rendering.
- [05-error-handling.md](05-error-handling.md) — common failure modes.
