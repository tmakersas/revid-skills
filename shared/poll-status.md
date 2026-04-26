# shared/poll-status

Canonical polling pseudocode every skill should call after `POST /render`.
Linked from each `SKILL.md` so we don't repeat it in every file.

```pseudo
function waitForRevid(pid, opts = { timeoutMs: 600_000 }):
  deadline = now() + opts.timeoutMs
  delay    = 5_000          # ms

  loop while now() < deadline:
    body = GET /api/public/v3/status?pid=$pid
           with header `key: $REVID_API_KEY`

    if body.status == "ready":
      return body                     # body.videoUrl present
    if body.status == "failed":
      throw Error(body.error or "render failed")

    sleep(delay)
    if body.progress > 30: delay = 8_000

  throw TimeoutError("pid $pid not ready after $opts.timeoutMs ms")
```

Concrete implementations: [Python](../docs/03-polling-and-webhooks.md#reference-python-loop)
· [TypeScript](../docs/03-polling-and-webhooks.md#reference-typescript-loop).

In production prefer a `webhookUrl` over polling — see
[03-polling-and-webhooks.md §B](../docs/03-polling-and-webhooks.md#b-webhooks-preferred-for-production).
