# Foundry Agent Service — session site

A navigable static site that publishes the content of the session deck
*Foundry Agent Service* (Session 1 of 3, Day 1 — delivered for RAI Pubblicità).
Built from `Foundry_Agent_Service( wn).pptx` — 54 slides, last saved 8 September 2026.

Same shape as the AI Evaluation site: a landing page plus one page per module under
`sessions/`, generated from a single source of truth — the PowerPoint deck.

## Structure

```
site/
├── index.html                          landing page: pillars, module cards, programme, Day 2 labs
├── sessions/
│   ├── 00-orientation.html             slides 1–5    how the two days work, agenda, rhythm, vision
│   ├── 01-vision-architecture.html     slides 6–14   why agents now, what Foundry is, the reference map
│   ├── 02-foundry-agent-service.html   slides 15–29  runtime, MCP/A2A, Toolbox, memory, Entra Agent ID, Voice Live
│   ├── 03-four-iqs.html                slides 30–38  Work IQ, Foundry IQ, Web IQ, Fabric IQ
│   ├── 04-agent-365.html               slides 39–50  fleet governance, identity, publishing to Teams
│   └── 05-wrap-up.html                 slides 51–54  the whole story, takeaways by role, Day 2 labs
├── build/
│   ├── build_site.py                   regenerates the whole site from the .pptx
│   └── slidehtml.py                    rebuilds each slide's visual layout as scalable HTML
└── README.md
```

Each topic is published twice over: first the **slide itself**, rebuilt as scalable HTML —
same layout, colours, panels, arrows, tables and pictures as the deck, scaling with the
browser width and keeping every word as selectable, searchable, translatable text — and
below it a collapsible **"Slide text"** block (closed by default) for fast reading and
copy/paste.

Every page is a single self-contained HTML file: inline CSS, images embedded as data URIs,
no JavaScript, no external requests. Copy the folder anywhere — a web server, SharePoint,
a USB stick — and it works. Dark mode and print stylesheets are included.

**Speaker notes are never published.** The build reads them from the deck and deliberately
drops them; only what is on the slides reaches the site.

## Publish it

Locally:

```bash
python -m http.server 8000 --directory site
# open http://localhost:8000
```

GitHub Pages: commit the folder, then set *Settings → Pages → Source* to the branch and
the folder. No build step is required on the server — the HTML is already final.

## Regenerate after editing the deck

```bash
pip install python-pptx pillow
DECK="Foundry_Agent_Service( wn).pptx" OUT=site python build/build_site.py
```

To change how slides are grouped into modules — titles, one-line descriptions, tags, slide
ranges — edit the `MODULES` list at the top of `build/build_site.py` and rebuild. The site
design lives in the `CSS` string in the same file; slide-rendering rules live in
`slidehtml.py`.

## Source

Deck: `Foundry_Agent_Service( wn).pptx` — 54 slides, 6 live demos.
Author: Mauro Minella, Senior Cloud Solution Architect, Microsoft.
