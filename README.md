# Revid Agentic Skills

Drop-in agent skills that turn any link, blog, product, article, tweet, PDF, or
one-line idea into a finished short-form video — by calling the
[Revid Public API v3](https://documenter.getpostman.com/view/36975521/2sBXcGEfaB).

**11 skills · works with OpenClaw, Claude Skills, Codex, Cursor, Gemini CLI, and
any agent that reads `SKILL.md`.**

- 🌐 Marketplace: <https://revid-skills.vercel.app>
- 📦 ClawHub: <https://clawhub.ai/@api00>
- 🛠 Source: this repo (MIT-licensed)

---

## Install in 30 seconds

### 1. Get a Revid API key

Sign up at <https://www.revid.ai/account>, copy your key, then once per machine:

```bash
export REVID_API_KEY="rk_live_…"
```

Every skill gates on this. No key, no render.

### 2. Install one skill — pick your agent

| Agent | Install |
|---|---|
| **OpenClaw** *(native)* | `openclaw skills install revid-shopify-product-promo` |
| **Claude Skills** | `npx degit tmakersas/revid-skills/skills/revid-shopify-product-promo ~/.claude/skills/revid-shopify-product-promo` |
| **Codex** | `curl -fsSL https://raw.githubusercontent.com/tmakersas/revid-skills/main/skills/revid-shopify-product-promo/SKILL.md >> AGENTS.md` |
| **Cursor** | `curl -fsSL …/SKILL.md >> .cursorrules` |
| **Gemini CLI** | `curl -fsSL …/SKILL.md -o GEMINI.md` |
| **Anything else** | `curl -fsSL …/SKILL.md` and paste into the agent's context |

### 3. Ask the agent

```
Use Shopify Product Promo to turn https://allbirds.com/products/mens-tree-runners into a TikTok
```

The skill will scrape the URL, build the right `POST /render` payload, poll
`GET /status`, and hand back an MP4 URL — typically in 2–4 minutes, ~40 credits.

---

## The 11 skills

| Skill | Input | Output | Revid workflow |
|---|---|---|---|
| [`revid-api-foundations`](skills/revid-api-foundations/SKILL.md) | — *(read first)* | — | foundation |
| [`revid-shopify-product-promo`](skills/revid-shopify-product-promo/SKILL.md) | Shopify / e-com product URL | 30–45 s 9:16 promo | `article-to-video` |
| [`revid-blog-to-avatar-video`](skills/revid-blog-to-avatar-video/SKILL.md) | Blog post URL + avatar image | Talking-head avatar video | `article-to-video` + avatar block |
| [`revid-article-to-short`](skills/revid-article-to-short/SKILL.md) | News / long-form URL | 30–60 s 9:16 short | `article-to-video` |
| [`revid-product-description-to-ad`](skills/revid-product-description-to-ad/SKILL.md) | Product copy (free text) | 15–30 s ad with hook + CTA | `ad-generator` |
| [`revid-tweet-to-talking-head`](skills/revid-tweet-to-talking-head/SKILL.md) | Tweet / thread URL or text | 20–45 s talking-head | `script-to-video` + avatar |
| [`revid-script-to-video`](skills/revid-script-to-video/SKILL.md) | Pre-written script | Voiceover + auto-cut visuals | `script-to-video` |
| [`revid-prompt-to-video`](skills/revid-prompt-to-video/SKILL.md) | One-line idea | AI-written script + video | `prompt-to-video` |
| [`revid-pdf-to-video`](skills/revid-pdf-to-video/SKILL.md) | PDF URL | 30–90 s summary video | `article-to-video` |
| [`revid-news-to-daily-short`](skills/revid-news-to-daily-short/SKILL.md) | Topic / niche | Daily news short (live news) | `article-to-video` w/ `fetchNews=true` |
| [`revid-script-with-custom-media`](skills/revid-script-with-custom-media/SKILL.md) | Script + your own clips | Branded video, no stock | `script-to-video` w/ `useOnlyProvided` |

---

## How a skill works

Every `SKILL.md` is plain Markdown with YAML frontmatter — no SDK, no runtime
lock-in. The shape is uniform across all 11:

```markdown
---
name: revid-shopify-product-promo
description: One-paragraph "when to invoke this and what it does"
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---

## When to use this skill
## Inputs
## Step-by-step
## API call template     ← the JSON body to POST
## Polling               ← inlined, ~10 lines of bash
## Failure modes         ← table of error → fix
## See also
```

The agent reads the markdown, fills in `{PRODUCT_URL}` / `{SCRIPT}` /
`{AVATAR_URL}` / etc. from the user's request, sends the call, and waits.

---

## Repository layout

```
.
├── skills/                  # the 11 SKILL.md skill folders
│   └── <slug>/
│       ├── SKILL.md         # the prompt agents load
│       └── examples/        # runnable JSON payload + run.sh
├── site/                    # Next.js marketplace UI (deployed to Vercel)
├── docs/                    # full Revid API v3 reference
├── examples/                # standalone curl / Python / TypeScript clients
├── shared/                  # cross-skill snippets (polling pseudocode etc.)
├── PUBLISHING.md            # how to publish updates to ClawHub
└── TODO.md                  # v1.1 backlog (watcher skills, agentic flows)
```

---

## Local smoke test (no agent required)

Every skill ships a `run.sh` that exercises it via plain curl:

```bash
export REVID_API_KEY="rk_live_…"
cd skills/revid-shopify-product-promo
./examples/run.sh https://allbirds.com/products/mens-tree-runners
# → submits the render, polls until ready, prints videoUrl
```

---

## Publishing updates to ClawHub

Maintainer-only. See [`PUBLISHING.md`](PUBLISHING.md) for the full workflow.
TL;DR:

```bash
clawhub login
clawhub publish ./skills/<slug> --slug <slug> --name "Display Name" --version 1.0.1
```

Auto-updates on installed agents the next time they sync.

---

## Roadmap

See [`TODO.md`](TODO.md). Highlights:

- **Watcher skills** (`revid-blog-watcher`, `revid-shopify-watcher`,
  `revid-news-watcher`, `revid-x-thread-watcher`) — poll a feed, dedupe, fire
  the right base skill on each new item. Closes the *"watch and react"* gap
  identified in v1 review.
- **Pro tier** (`revid-*-pro`) using `videoModel: veo3` / `sora2` for premium
  output.
- **Optional enrichment proxy** that uses our OpenAI key to auto-craft
  `scrapingPrompt` + `stylePrompt` per URL — under evaluation.

---

## Links

- **Live site** — <https://revid-skills.vercel.app>
- **Revid API spec** — <https://documenter.getpostman.com/view/36975521/2sBXcGEfaB>
- **Revid Studio** (build manually, then "Get API code") — <https://www.revid.ai/create>
- **OpenClaw** — <https://openclaw.ai>
- **ClawHub** — <https://clawhub.ai>

---

## License

MIT. Fork the repo, adapt SKILL.md for any agent runtime — that's the point.
