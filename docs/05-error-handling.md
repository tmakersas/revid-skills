# 05 · Error handling

## Response shape

Every render endpoint returns a JSON envelope:

```json
{ "success": 1, "pid": "…", … }   // success
{ "success": 0, "error": "…" }    // failure
```

Skills should treat `success !== 1` as a hard error and surface `error` to the
caller verbatim.

## HTTP-level errors

| Code | Cause | Fix |
|---|---|---|
| `401` | Missing or wrong `key` header | Re-export `REVID_API_KEY`. |
| `402` / `403` | Out of credits or plan-locked feature | Top up; downgrade `media.quality`; remove `videoModel: "veo3"/"sora2"`. |
| `404` (on `/status`) | Unknown `pid` | Verify the `pid` returned by `/render`. |
| `409` | Project state conflict | Project may already be queued/exporting; wait or use a new `projectId`. |
| `422` | Schema violation | Compare the request body to [02-api-reference.md](02-api-reference.md). |
| `429` | Rate-limited | Back off (5–10 s) and retry. |
| `5xx` | Transient | Retry with exponential backoff (max 3). |

## Render-state errors (status = `failed`)

`GET /status` may return `status: "failed"` with an `error` string:

| `error` substring | Likely cause | Recovery |
|---|---|---|
| `scrape failed` / `403` from source | URL is JS-only or blocks bots | Pass `source.scrapingPrompt` with a manual title/body, or fetch the content yourself and switch to `script-to-video`. |
| `script too long` | Content exceeded model context | Set `options.summarizationPreference: "summarize"` or shorten input. |
| `voice unavailable` | Bad `voice.voiceId` | Use a known voice or omit to fall back. |
| `nsfw content detected` | Source / generated text triggered filter | Toggle `options.nsfwFilter: false` if your plan allows; otherwise rephrase. |
| `media generation timed out` | Heavy `videoModel` under load | Drop to `pro` / `base` and retry. |
| `unknown workflow` | Typo in `workflow` field | See enum in [02-api-reference.md](02-api-reference.md). |

## Defensive client-side checks

Before calling `/render`, validate:

1. **API key set** — fail fast if `REVID_API_KEY` is empty.
2. **`workflow` is one of the known enum values.**
3. **The right `source` field is filled** for the workflow:
   - `text` → `script-to-video`
   - `prompt` → `prompt-to-video`, `ad-generator`
   - `url` → `article-to-video`, `music-to-video`, `caption-video`,
     `motion-transfer`
4. **`aspectRatio` matches the consumer surface** (`9:16` for Reels/TikTok/Shorts;
   `16:9` for YouTube long-form; `1:1` for feed posts).
5. **Estimate credits first** if cost matters — see
   [04-credits-and-pricing.md](04-credits-and-pricing.md).

## Skill-level retry policy

When polling, retry transient `5xx` and `429` from `/status` (up to 3 times) but
do **not** retry `failed` renders silently — bubble the error up so the caller
can decide whether to regenerate with different parameters.

## See also

- [03-polling-and-webhooks.md](03-polling-and-webhooks.md) for the wait pattern.
- Each `skills/<name>/SKILL.md` ends with a `## Failure modes` section listing
  workflow-specific gotchas.
