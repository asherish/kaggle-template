---
name: kaggle-browse
user-invocable: true
description: "Browse Kaggle pages (competitions, notebooks, discussions, leaderboards) with authenticated access via MCP Playwright. Use this skill whenever the user wants to view, read, or extract information from Kaggle web pages — including competition overviews, notebook code/output/figures, discussion threads, leaderboard standings, or any Kaggle content. Also trigger when the user shares a Kaggle URL, asks about a competition's rules/evaluation/timeline/prizes, says 'check Kaggle', 'look at that notebook', or 'what's the leaderboard look like'."
argument-hint: "[url or description of what to browse]"
allowed-tools:
  - mcp__plugin_playwright_playwright__browser_navigate
  - mcp__plugin_playwright_playwright__browser_snapshot
  - mcp__plugin_playwright_playwright__browser_take_screenshot
  - mcp__plugin_playwright_playwright__browser_wait_for
  - mcp__plugin_playwright_playwright__browser_click
  - mcp__plugin_playwright_playwright__browser_run_code
  - mcp__plugin_playwright_playwright__browser_press_key
  - Bash
  - Read
---

# Browsing Kaggle with MCP Playwright

Kaggle is a single-page app (SPA) — standard HTTP fetching returns empty HTML because content is rendered via JavaScript. This skill uses MCP Playwright to run a real browser with authenticated session cookies.

## Prerequisites

- **Session cookies**: `~/.kaggle/playwright_state.json`
  - Created by: `uv run tools/kaggle_login.py`
- **API token** (optional): `~/.kaggle/access_token`

If cookies are missing or expired, tell the user to run `uv run tools/kaggle_login.py`.

## Step 1: Inject Cookies and Navigate

Every session starts by loading cookies. This is a two-step process because `browser_run_code` runs inside the browser (not Node.js), so it cannot read local files directly.

**Step 1a**: Read cookies from the JSON file using Bash:

```bash
cat ~/.kaggle/playwright_state.json | python3 -c "import json,sys; print(json.dumps(json.load(sys.stdin)['cookies']))"
```

**Step 1b**: Pass the cookie array into `browser_run_code` to inject and navigate:

```javascript
async (page) => {
  const cookies = PASTE_COOKIE_ARRAY_HERE;
  await page.context().addCookies(cookies);
  await page.goto('TARGET_URL', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(8000);
  return await page.title();
}
```

Replace `PASTE_COOKIE_ARRAY_HERE` with the JSON array from Step 1a, and `TARGET_URL` with the Kaggle URL.

**Critical**: Do NOT use `waitUntil: "networkidle"` — it times out on Kaggle. Always use `"domcontentloaded"` + `waitForTimeout(8000)`.

Once cookies are injected, subsequent navigations within the same session can use `browser_navigate` + `browser_wait_for` (time: 8) without re-injecting cookies.

## Step 2: Extract Content

### Text content → `browser_snapshot`

Captures all rendered text: competition info, discussion posts, notebook code and text output.

### Visual content → `browser_take_screenshot`

Use with `fullPage: true` for notebook figures, charts, and plots. The snapshot cannot capture images.

### Navigate tabs/pages → `browser_click`

Click tab elements (Overview, Data, Code, Discussion, Leaderboard, Rules) or pagination buttons using refs from the snapshot.

## Page-Specific Notes

### Competition overview (`/competitions/SLUG/overview`)
- Contains: Description, Evaluation, Timeline, Prizes, Compute info
- All sections are in the snapshot after a single page load
- Works without login

### Discussion (`/competitions/SLUG/discussion` or `.../discussion/TOPIC_ID`)
- Thread list and full thread content available in snapshot
- Works without login

### Notebooks (`/code/USER/SLUG`)
- **Requires login cookies**
- Content renders inside an iframe — snapshot captures it with refs like `f10eXXX`
- For figures: use `browser_take_screenshot` with `fullPage: true`
- For long notebooks: scroll with `browser_press_key` (PageDown)

### Code tab (`/competitions/SLUG/code`)
- Notebook list may show as `undefined List Item` in snapshot
- Use screenshot as fallback

## Kaggle API (Optional, Faster for Structured Data)

Read the token from `~/.kaggle/access_token` and use as Bearer token:

```bash
TOKEN=$(cat ~/.kaggle/access_token)

# Competition info
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.kaggle.com/api/v1/competitions/list?search=SLUG"

# Notebook list
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.kaggle.com/api/v1/kernels/list?competition=SLUG&sortBy=voteCount&pageSize=10"

# Notebook source code (no output/figures)
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://www.kaggle.com/api/v1/kernels/pull?userName=USER&kernelSlug=SLUG"
```

## Quick Reference: Which Method to Use

| Content | Best Method |
|---------|------------|
| Competition overview/rules/evaluation | Playwright snapshot |
| Discussion threads | Playwright snapshot |
| Notebook list | Kaggle API |
| Notebook source code only | Kaggle API |
| Notebook output + figures | Playwright screenshot |
| Leaderboard | Playwright snapshot |
