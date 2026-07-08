
# Tracéa Backend

Generate premium SVG posters from GPX activities.

## Stack

- Python 3.12
- FastAPI
- Uvicorn
- Pydantic
- PyProj
- Shapely
- SVGWrite

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

## Start the API

```bash
uvicorn app.main:app --reload
```

## API documentation

[http://127.0.0.1:8000/docs]()

Pipeline

<pre class="overflow-visible! px-0!" data-start="616" data-end="761"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>GPX file</span><br/><span>    ↓</span><br/><span>GPX Parser</span><br/><span>    ↓</span><br/><span>Activity model</span><br/><span>    ↓</span><br/><span>Track simplification</span><br/><span>    ↓</span><br/><span>Geographic projection</span><br/><span>    ↓</span><br/><span>SVG Renderer</span><br/><span>    ↓</span><br/><span>SVG Poster</span></code></pre></div></div></div></div></div></div></div></div></div><div class=""><div class=""></div></div></div></div></div></div></pre>

## Project structure

<pre class="overflow-visible! px-0!" data-start="785" data-end="1053"><div class="relative w-full mt-4 mb-1"><div class=""><div class="contents"><div class="relative"><div class="h-full min-h-0 min-w-0"><div class="h-full min-h-0 min-w-0"><div class="border border-token-border-light border-radius-3xl corner-superellipse/1.1 rounded-3xl"><div class="h-full w-full border-radius-3xl bg-token-bg-elevated-secondary corner-superellipse/1.1 overflow-clip rounded-3xl lxnfua_clipPathFallback"><div class="pointer-events-none absolute end-1.5 top-1 z-2 md:end-2 md:top-1"></div><div class="relative"><div class="pe-11 pt-3"><div class="relative z-0 flex max-w-full"><div id="code-block-viewer" dir="ltr" class="q9tKkq_viewer cm-editor z-10 light:cm-light dark:cm-light flex h-full w-full flex-col items-stretch ͼs ͼ16"><div class="cm-scroller"><pre class="cm-content q9tKkq_readonly m-0"><code><span>app/</span><br/><span>├── api/          # FastAPI routes</span><br/><span>├── models/       # Business and API models</span><br/><span>├── services/     # Application logic</span><br/><span>├── gpx/          # GPX parsing</span><br/><span>├── geo/          # Geographic processing</span><br/><span>├── svg/          # SVG generation</span><br/><span>└── utils/        # Utilities</span></code></pre></div></div></div></div></div></div></div></div></div></div></div></div></div></pre>
