# Revid

The `revid` MCP server (`https://www.revid.ai/api/mcp`) researches what goes viral, makes finished
short-form videos and posts them to TikTok, YouTube, Instagram and X. Sign in once with `/mcp auth revid`.

- Research before writing: `search_viral_videos` costs no credits.
- Price before rendering: `calculate_credits` with the exact `render_video` payload.
- `render_video` returns a `pid`; poll `get_project_status` every 20 to 30 seconds until `videoUrl`.
- For background music, set `music: { generateMusic: true }` rather than a library track.
- Posting is public: confirm the account, caption and time before `publish_now` or `schedule_publish`.

The skills in `skills/` cover each workflow step by step (start with `revid-research-make-and-post`).
