# Publishing Revid skills to ClawHub

This is the one-time setup + per-release workflow for getting all 11 Revid
skills onto [ClawHub](https://clawhub.ai) so OpenClaw users can install them
with `openclaw skills install <slug>`.

## 1. One-time setup

### 1.1 Install the OpenClaw + ClawHub CLI

```bash
# OpenClaw runtime (skips if you already have it)
npm i -g openclaw
# or: curl -fsSL https://openclaw.ai/install.sh | sh

# ClawHub publishing CLI (lives inside OpenClaw)
clawhub --version   # should print a version
```

If `clawhub` is missing, follow https://docs.openclaw.ai/cli/skills.md.

### 1.2 Sign in to ClawHub

```bash
clawhub login
```

> ClawHub requires a GitHub account that is **at least one week old** to
> publish — this is anti-abuse, not a paywall.

### 1.3 Confirm every SKILL.md frontmatter is correct

Each skill folder under `skills/` must have a `SKILL.md` with this minimum
frontmatter (already applied to all 11 skills in this repo):

```markdown
---
name: revid-shopify-product-promo
description: One-line summary the agent will read.
metadata: {"openclaw":{"requires":{"config":["REVID_API_KEY"]}}}
---
```

The `metadata.openclaw.requires.config` block tells OpenClaw to refuse to load
the skill until the user has `REVID_API_KEY` set in their environment.

## 2. Publish every skill

### Easiest: one command, all 11 at once

```bash
cd /Users/apialam/Desktop/WORK/TMAKER/revid-workflow
clawhub sync --dry-run    # preview
clawhub sync --all        # publish for real
```

`clawhub sync` scans `skills/` and publishes anything new or updated.

### Manual: one-by-one (use this if you need custom names/versions)

Versioning uses semver. From the repo root:

```bash
cd skills

# foundation (load this first, every other skill depends on it)
clawhub publish ./revid-api-foundations \
  --slug revid-api-foundations \
  --name "Revid API Foundations" \
  --version 1.0.0

clawhub publish ./revid-shopify-product-promo \
  --slug revid-shopify-product-promo \
  --name "Shopify Product Promo" \
  --version 1.2.0

clawhub publish ./revid-blog-to-avatar-video \
  --slug revid-blog-to-avatar-video \
  --name "Blog → Avatar Video" \
  --version 1.1.0

clawhub publish ./revid-article-to-short \
  --slug revid-article-to-short \
  --name "Article → Short" \
  --version 1.3.0

clawhub publish ./revid-product-description-to-ad \
  --slug revid-product-description-to-ad \
  --name "Product Description → Ad" \
  --version 1.0.1

clawhub publish ./revid-tweet-to-talking-head \
  --slug revid-tweet-to-talking-head \
  --name "Tweet → Talking-Head" \
  --version 1.0.0

clawhub publish ./revid-script-to-video \
  --slug revid-script-to-video \
  --name "Script → Video" \
  --version 1.4.0

clawhub publish ./revid-prompt-to-video \
  --slug revid-prompt-to-video \
  --name "Prompt → Video" \
  --version 1.2.0

clawhub publish ./revid-pdf-to-video \
  --slug revid-pdf-to-video \
  --name "PDF → Video" \
  --version 1.0.0

clawhub publish ./revid-news-to-daily-short \
  --slug revid-news-to-daily-short \
  --name "Daily News Short" \
  --version 1.1.0

clawhub publish ./revid-script-with-custom-media \
  --slug revid-script-with-custom-media \
  --name "Script + Custom Media" \
  --version 1.0.0
```

ClawHub assigns the version, hashes the bundle, and makes it discoverable from
`openclaw skills search revid`.

## 3. End-user install flow (what your users will do)

```bash
# one-time, per machine
export REVID_API_KEY="rk_live_..."

# install any Revid skill
openclaw skills install revid-shopify-product-promo

# then in the OpenClaw chat:
# "Use Shopify Product Promo to turn https://shop.example.com/p/aeropods into a TikTok"
```

## 4. Releasing a new version

```bash
# bump SKILL.md if needed (description/metadata changes), then:
clawhub publish ./revid-shopify-product-promo \
  --slug revid-shopify-product-promo \
  --name "Shopify Product Promo" \
  --version 1.2.1
```

Existing installs upgrade automatically the next time the user runs
`openclaw skills update --all` (or whenever the auto-updater fires).

## 5. Smoke-test locally without publishing

You can sideload any skill folder before pushing to ClawHub:

```bash
# from your OpenClaw workspace root
mkdir -p skills
cp -R /path/to/revid-workflow/skills/revid-shopify-product-promo skills/
# OpenClaw will pick it up on the next session
openclaw skills list
```

Workspace skills take precedence over ClawHub-installed ones, which is the
safest way to test changes before bumping a version.
