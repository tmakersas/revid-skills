# 01 · Getting started

## 1. Get an API key

1. Sign in at <https://www.revid.ai>.
2. Open **Account → API**.
3. Copy the key. Store it as `REVID_API_KEY` — never check it in.

```bash
export REVID_API_KEY="sk_live_…"
```

## 2. Sanity-check the key

The simplest valid render call: `prompt-to-video` with one line of text.

```bash
curl -s https://www.revid.ai/api/public/v3/render \
  -H "Content-Type: application/json" \
  -H "key: $REVID_API_KEY" \
  -d '{
    "workflow": "prompt-to-video",
    "source":   { "prompt": "A 30-second short about why honey never spoils." },
    "aspectRatio": "9:16"
  }'
```

Expected response:

```json
{
  "success": 1,
  "pid": "p_abc123…",
  "workflow": "prompt-to-video",
  "endpoint": "/api/public/v3/render",
  "docs": { … }
}
```

If you get `{"success": 0, "error": "Invalid API key"}` your key is wrong or
unset.

## 3. Wait for the video

```bash
curl -s "https://www.revid.ai/api/public/v3/status?pid=p_abc123…" \
  -H "key: $REVID_API_KEY"
```

Poll every ~5 s until `status` becomes `ready` (or `failed`). See
[03-polling-and-webhooks.md](03-polling-and-webhooks.md) for the production
pattern.

## 4. Pick a skill

Once your key works, jump to a skill in `skills/` that matches the input you
have. Skills are self-contained — you don't have to read the whole API spec to
use one.

---

**Next:** [02-api-reference.md](02-api-reference.md) for the full schema, or any
skill in [`skills/`](../skills/) for a worked example.
