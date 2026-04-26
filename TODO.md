# Revid Skills — TODO / v1.1 backlog

Tracking gaps between tibo's brief (Slack, 2026-04-24) and the v1 catalog.
Resolved items live in git history; only open work is listed here.

## Open: agentic / watcher skills (v1.1)

tibo's brief asked for "watch a blog and create an avatar video for **every
new** blog post" and probed "do you want anything agentic?" Our v1 ships 11
*transform* skills (one input → one video). The watch / monitor / react half
is missing. Add as a follow-up release once v1 catalog is live.

### Skills to add

- [ ] `revid-blog-watcher` — poll an RSS feed or sitemap, dedupe against a
      seen-list at `~/.openclaw/state/revid-blog-watcher/seen.json`, hand each
      new post to `revid-blog-to-avatar-video`. Cron-friendly.

- [ ] `revid-shopify-watcher` — diff a Shopify storefront's `/products.json`
      feed against a seen-list, fire `revid-shopify-product-promo` for each new
      product launch.

- [ ] `revid-news-watcher` — same shape as blog-watcher but for a topic feed
      (Google News RSS / niche aggregators), routes new items into
      `revid-news-to-daily-short`.

- [ ] `revid-x-thread-watcher` — watch a creator's X / Twitter handle for new
      threads, route into `revid-tweet-to-talking-head` automatically.

### Cross-cutting work for the watcher family

- [ ] Shared **dedupe / seen-list** convention. Probably a small shared helper
      docs page (not a skill) that documents the on-disk format every watcher
      reuses.
- [ ] Shared **cron / scheduling** snippets — crontab, GitHub Actions cron,
      Vercel Cron, OpenClaw's own scheduler. One canonical example linked from
      every watcher skill.
- [ ] **Idempotency** — calling the same render twice for the same source
      shouldn't burn double credits. Add `metadata.sourceId` checks before
      `POST /render`.
- [ ] **Failure-state handling** — if a render fails, retry once with
      `media.quality` downgraded; log the failure to a local audit file.

## Open: marketplace site polish (v1.1)

- [ ] **"Verified on ClawHub" badge** on each skill card once we confirm the
      install count + version match what's published on clawhub.ai.
- [ ] **Real install counts** — currently catalog.ts has hand-set numbers.
      Wire to `GET /api/skills/<slug>` on ClawHub once that endpoint exists.
- [ ] **Source link** on each detail page → real GitHub URL once the repo is
      pushed publicly.
- [ ] **Web preview of rendered video** — show a 5–8 s sample MP4 inline on
      each skill detail page so the catalog *demonstrates* what it ships.

## Open: docs

- [ ] **Quickstart screencast** — 60 s clip showing
      `openclaw skills install revid-shopify-product-promo` end-to-end and the
      resulting video, embedded on the home page.
- [ ] **Per-skill pricing estimate** — wire each detail page to
      `POST /api/public/v3/calculate-credits` with the skill's default payload
      so users see "≈ $0.18 per render" before they install.

## Done in v1 (do not re-do)

- [x] 11 SKILL.md files with valid frontmatter + `REVID_API_KEY` config gate
- [x] All `source.*` fields match Revid OpenAPI workflow contract
- [x] Self-contained — no dead `../../shared/`, `../../docs/`, or
      `../../examples/` cross-folder references
- [x] Working `examples/run.sh` per skill (executable, self-contained)
- [x] Marketplace site at `site/` with detail pages, install buttons, file
      viewer, related skills
- [x] Real `openclaw skills install <slug>` command wired through the UI
- [x] `PUBLISHING.md` with the 11 publish commands
