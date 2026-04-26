# 04 · Credits and pricing

Every render costs credits. Estimate **before** you spend.

## Estimate without rendering

```bash
curl -s https://www.revid.ai/api/public/v3/calculate-credits \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d '{
    "workflow":   "article-to-video",
    "source":     { "url": "https://blog.example.com/launch" },
    "aspectRatio": "9:16",
    "render":     { "resolution": "1080p" },
    "media":      { "quality": "pro", "videoModel": "pro" }
  }'
```

Response:

```json
{
  "creditsEstimate": 4,
  "breakdown": {
    "base": 1,
    "voice": 1,
    "visualsModel": 1,
    "resolution": 1
  }
}
```

## Knobs that drive cost

| Knob | Cheap | Expensive |
|---|---|---|
| `media.quality` / `imageModel` / `videoModel` | `cheap` / `base` | `ultra` / `veo3` / `sora2` |
| `render.resolution` | `720p` | `4k` |
| `options.outputCount` | 1 | many variants |
| Length (`durationSeconds`, `targetDuration`) | shorter | longer |
| `media.density` | `low` | `high` |
| `avatar` enabled? | no | yes (extra) |
| `music.generateMusic` | no | yes |

## Practical defaults per skill

| Skill | Resolution | Quality | ~Credits |
|---|---|---|---|
| Quick draft / preview | `720p` | `cheap` / `base` | 1–2 |
| Standard short (most skills) | `1080p` | `pro` / `pro` | 2–4 |
| Premium ad / hero | `1080p` | `ultra` / `ultra` | 5–8 |
| Cinematic showcase | `4k` | `ultra` / `veo3`/`sora2` | 10+ |

Skill SKILL.md files default to **standard** (`1080p` + `pro`) unless they say
otherwise.

## Top up

```bash
curl -s https://www.revid.ai/api/public/v3/buy-credit-pack \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d '{ "packId": "credits_500" }'
```

## See also

- [02-api-reference.md](02-api-reference.md)
- [05-error-handling.md](05-error-handling.md) — `insufficient_credits` is the
  most common avoidable failure.
