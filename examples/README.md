# Examples

Runnable scripts that exercise the skills in `../skills/`. Each script is
self-contained — only `REVID_API_KEY` and the per-skill input args are needed.

```
examples/
├── curl/                # plain bash + curl + jq
│   ├── render-prompt.sh
│   ├── estimate-credits.sh
│   └── list-projects.sh
├── python/              # all share revid_client.py
│   ├── revid_client.py  # tiny shared client (auth + render + poll + estimate)
│   ├── shopify_product.py
│   ├── blog_to_avatar.py
│   ├── prompt_to_video.py
│   └── news_daily.py
├── typescript/          # all share revidClient.ts
│   ├── revidClient.ts
│   ├── articleToShort.ts
│   └── productAd.ts
└── payloads/            # standalone JSON for `curl -d @file`
    ├── minimal-prompt.json
    ├── minimal-script.json
    ├── minimal-article.json
    ├── minimal-ad.json
    └── minimal-avatar.json
```

## Quickstart

```bash
export REVID_API_KEY="sk_…"

# Smallest possible call:
chmod +x examples/curl/render-prompt.sh
examples/curl/render-prompt.sh "Why honey never spoils."

# Python:
pip install requests
python examples/python/prompt_to_video.py "Why honey never spoils."

# TypeScript:
npx tsx examples/typescript/articleToShort.ts https://blog.example.com/post
```

## Per-skill examples

Each `skills/<name>/examples/` folder also contains the canonical payload + a
`run.sh` for that workflow. Those are the ones to read first when learning a
specific skill.
