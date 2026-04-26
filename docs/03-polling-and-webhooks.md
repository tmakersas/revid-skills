# 03 · Polling and webhooks

`POST /render` returns *immediately* with a `pid`. Rendering takes 30 s – 5 min
depending on length, model quality, and queue depth. There are two ways to wait:

## A. Polling (default)

Hit `GET /api/public/v3/status?pid={pid}` every few seconds.

```bash
curl -s "https://www.revid.ai/api/public/v3/status?pid=$PID" \
  -H "key: $REVID_API_KEY"
```

Response shape (typical):

```json
{
  "pid": "p_…",
  "status": "queued" | "rendering" | "ready" | "failed",
  "progress": 0..100,
  "videoUrl": "https://cdn.revid.ai/v/…mp4",   // present when ready
  "thumbnailUrl": "https://cdn.revid.ai/t/…jpg",
  "durationSeconds": 38,
  "creditsUsed": 1,
  "error": "…"                                  // present when failed
}
```

### Recommended polling cadence

| Phase | Cadence | Why |
|---|---|---|
| `queued` | every 5 s | usually clears in < 10 s |
| `rendering` 0–30 % | every 5 s | most failures surface early |
| `rendering` 30–95 % | every 8 s | be polite |
| `ready` / `failed` | stop | terminal |

Add a hard timeout (e.g. 10 minutes) in case of stuck jobs.

### Reference Python loop

```python
import os, time, requests

API = "https://www.revid.ai/api/public/v3"
KEY = os.environ["REVID_API_KEY"]

def wait_for(pid: str, timeout_s: int = 600) -> dict:
    deadline = time.time() + timeout_s
    delay = 5
    while time.time() < deadline:
        r = requests.get(f"{API}/status",
                         params={"pid": pid},
                         headers={"key": KEY},
                         timeout=15)
        r.raise_for_status()
        body = r.json()
        if body.get("status") == "ready":
            return body
        if body.get("status") == "failed":
            raise RuntimeError(body.get("error", "render failed"))
        time.sleep(delay)
        if body.get("progress", 0) > 30:
            delay = 8
    raise TimeoutError(f"pid {pid} not ready after {timeout_s}s")
```

### Reference TypeScript loop

```ts
const API = "https://www.revid.ai/api/public/v3";
const KEY = process.env.REVID_API_KEY!;

export async function waitFor(pid: string, timeoutMs = 600_000) {
  const deadline = Date.now() + timeoutMs;
  let delayMs = 5000;
  while (Date.now() < deadline) {
    const res = await fetch(`${API}/status?pid=${pid}`, {
      headers: { key: KEY },
    });
    const body = await res.json();
    if (body.status === "ready") return body;
    if (body.status === "failed") throw new Error(body.error ?? "render failed");
    await new Promise((r) => setTimeout(r, delayMs));
    if ((body.progress ?? 0) > 30) delayMs = 8000;
  }
  throw new Error(`pid ${pid} not ready after ${timeoutMs} ms`);
}
```

## B. Webhooks (preferred for production)

Pass a public `webhookUrl` in the render request. Revid will `POST` the same
status payload (with `videoUrl`) when the job reaches a terminal state.

```json
{
  "workflow": "prompt-to-video",
  "source":   { "prompt": "Why honey never spoils." },
  "webhookUrl": "https://yourapp.com/hooks/revid"
}
```

Receiver responsibilities:

1. Respond `200 OK` quickly (under 5 s); handle work async.
2. Validate the `pid` against your records.
3. Treat duplicate deliveries as expected — make the handler idempotent.
4. Always cross-check by calling `/status?pid=…` once, in case the webhook
   payload was truncated or replayed.

### Skeleton (Express)

```ts
app.post("/hooks/revid", async (req, res) => {
  res.status(200).end();                           // ack first
  const { pid, status } = req.body;
  if (!pid) return;
  const truth = await fetch(
    `https://www.revid.ai/api/public/v3/status?pid=${pid}`,
    { headers: { key: process.env.REVID_API_KEY! } }
  ).then((r) => r.json());
  await onRevidUpdate(pid, truth);                 // your handler
});
```

## See also

- [02-api-reference.md](02-api-reference.md) — full schema.
- [05-error-handling.md](05-error-handling.md) — what `failed` actually means.
