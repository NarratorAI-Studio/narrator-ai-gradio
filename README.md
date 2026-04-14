---
title: Narrator AI
emoji: 🎬
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 6.12.0
app_file: app.py
pinned: false
---

# Narrator AI — Web UI

Web interface for [Narrator AI](https://www.jieshuo.cn/) — AI-powered video narration generation platform.

Select a movie, pick a narration style, choose a voice and BGM — get a complete narration video. No manual editing required.

## Features

**One-Click Generate** — Wizard mode that chains the full pipeline automatically:
- Select from 93 pre-built movie materials
- 80+ narration style templates across 12 genres
- 35 dubbing voices in 11 languages
- 30 background music tracks
- Real-time progress tracking via SSE streaming

**Task Management** — Query, list, and create tasks with full API control:
- Support for all 9 task types (popular-learning, generate-writing, fast-writing, clip-data, fast-clip-data, video-composing, magic-video, voice-clone, tts)
- Advanced JSON mode for power users
- SSE streaming support for real-time progress

**Library Browser** — Browse and search all available resources:
- Narration styles by genre (action, comedy, thriller, romance, sci-fi, etc.)
- Voice previews by language and tag
- BGM catalog

**Account** — Check balance and API key status

## Two Workflow Paths

| Path | Steps | Speed | Cost |
|------|-------|-------|------|
| **Recut** (二创文案) | popular-learning → generate-writing → clip-data → video-composing | Slower | Higher |
| **Original** (原创文案) | fast-writing → fast-clip-data → video-composing | Faster | Lower |

Both paths support an optional final step: **magic-video** (visual template application).

## Getting Started

### 1. Get an API Key

[Apply for an API key](https://ceex7z9m67.feishu.cn/share/base/form/shrcnmSHfAbYrFLsSeIrktEuYGf) (fill out the form, key will be issued after review).

### 2. Use the Web UI

Visit the hosted version: **[Narrator AI on HF Spaces](https://huggingface.co/spaces/NarratorAI-Studio/narrator-ai)**

Enter your API key in the top field, then use any tab.

### 3. Run Locally

```bash
git clone https://github.com/NarratorAI-Studio/narrator-ai-gradio.git
cd narrator-ai-gradio
pip install -r requirements.txt
python app.py
```

Open `http://localhost:7860` in your browser.

## Architecture

```
app.py          — Gradio UI (4 tabs: Wizard, Tasks, Library, Account)
client.py       — HTTP client for Narrator AI API (no CLI dependency)
data.py         — Static data: BGM, voices, narration styles, task endpoints
requirements.txt
```

The client communicates with the Narrator AI API via REST + SSE.

## CI/CD

Push to `main` triggers automatic deployment:

```
GitHub push → Blacksmith runner → HF Spaces
```

Workflow: [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NARRATOR_APP_KEY` | API key (alternative to UI input) | — |
| `NARRATOR_SERVER` | API server URL | `https://openapi.jieshuo.cn` |
| `NARRATOR_TIMEOUT` | Request timeout (seconds) | `60` |

## Related

- [Narrator AI](https://www.jieshuo.cn/) — Official website
- [Apply for API Key](https://ceex7z9m67.feishu.cn/share/base/form/shrcnmSHfAbYrFLsSeIrktEuYGf) — Key application form
- [API Docs](https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc) — Material previews, voice samples, BGM catalog

## License

MIT
