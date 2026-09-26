# Agentic AI on Microsoft Foundry — session site

A navigable static site that publishes the content of the session deck
*Agentic AI on Microsoft Foundry* (Session 3 of 3, Day 1 — delivered for RAI Pubblicità).
Built from `RAI_Agentic_Frameworks_on_Foundry_Day1 (wn).pptx` — 53 slides, last saved 26 September 2026.

Same shape as the other two session sites: a landing page plus one page per module under
`sessions/`, generated from a single source of truth — the PowerPoint deck.

## Structure

```
site/
├── index.html                            landing page: the four technologies, modules, programme, Day 2
├── sessions/
│   ├── 00-orientation.html               slides 1–8    welcome, the shift, why RAI, agenda, the four demos
│   ├── 01-agentic-landscape.html         slides 9–16   agent anatomy, the agentic loop, the Microsoft stack
│   ├── 02-agent-framework.html           slides 17–25  Microsoft Agent Framework, workflows, orchestration
│   ├── 03-foundry-hosted-agents.html     slides 26–32  Foundry platform, hosted agents, Agent Server, Toolkit
│   ├── 04-mcp.html                       slides 33–39  Model Context Protocol: primitives, ecosystem, security
│   ├── 05-a2a.html                       slides 40–46  Agent-to-Agent protocol, Agent Card, MCP vs A2A
│   └── 06-putting-it-together.html       slides 47–53  reference architecture, takeaways, bridge to Day 2
├── build/
│   ├── build_site.py                     regenerates the whole site from the .pptx
│   └── slidehtml.py                      rebuilds each slide's visual layout as scalable HTML
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
DECK="RAI_Agentic_Frameworks_on_Foundry_Day1 (wn).pptx" OUT=site python build/build_site.py
```

To change how slides are grouped into modules — titles, one-line descriptions, tags, slide
ranges — edit the `MODULES` list at the top of `build/build_site.py` and rebuild. The site
design lives in the `CSS` string in the same file; slide-rendering rules live in
`slidehtml.py`.

## Source

Deck: `RAI_Agentic_Frameworks_on_Foundry_Day1 (wn).pptx` — 53 slides, 4 live demos.
Author: Mauro Minella, Senior Cloud Solution Architect, Microsoft.
