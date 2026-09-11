# AI Evaluation in Microsoft Foundry — session site

A navigable static site that publishes the content of the session deck
*AI Evaluation in Microsoft Foundry* (Session 2 of 3, Day 1 — delivered for RAI Pubblicità).

Same shape as a GitHub Pages content portal: a landing page plus one page per module
under `sessions/`, generated from a single source of truth — the PowerPoint deck.

## Structure

```
site/
├── index.html                        landing page: pillars, module cards, programme, Day 2 labs
├── sessions/
│   ├── 00-orientation.html           slides 1–5    how the two days work, agenda, positioning
│   ├── 01-why-evaluation.html        slides 6–15   why evaluate, Responsible AI, GenAIOps, the platform
│   ├── 02-measure.html               slides 16–47  evaluators: quality, safety, agents, NLP, custom
│   ├── 03-generate.html              slides 48–61  Simulator, adversarial data, UPIA / XPIA
│   ├── 04-harden.html                slides 62–80  AI Red Teaming Agent, attack techniques, ASR
│   └── 05-code-appendix.html         slides 81–96  SDK code walkthroughs
├── build/
│   ├── build_site.py                 regenerates the whole site from the .pptx
│   └── slidehtml.py                  rebuilds each slide's visual layout as scalable HTML
└── README.md
```

Each topic is published twice over: first the **slide itself**, rebuilt as scalable HTML —
same layout, colours, panels, arrows, tables and pictures as the deck, scaling with the
browser width and keeping every word as selectable, searchable, translatable text — and
below it the plain-text version of the same slide for fast reading and copy/paste.

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
the `/site` folder. No build step is required on the server — the HTML is already final.

## Regenerate after editing the deck

```bash
pip install python-pptx pillow
DECK="AI-Evaluation-in-Microsoft-Foundry (wn).pptx" OUT=site python build/build_site.py
```

The script re-reads the deck, so slide edits flow straight through to the site.

To change how slides are grouped into modules — titles, one-line descriptions, tags,
slide ranges — edit the `MODULES` list at the top of `build/build_site.py` and rebuild.
The visual design lives in the `CSS` string in the same file.

## Source

Deck: `AI-Evaluation-in-Microsoft-Foundry (wn).pptx` — 96 slides.
Author: Mauro Minella, Senior Cloud Solution Architect, Microsoft.
