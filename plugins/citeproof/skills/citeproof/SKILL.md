---
name: citeproof
description: Write academic or professional documents (reports, essays, research papers, state-of-the-art reviews, theoretical frameworks, university assignments) where every claim is backed by a verifiable, recognizable source, cited in APA 7 or IEEE, and paired with proof the reader can check — either an automatic screenshot of the exact passage or a highlighted "capture note" with a clickable link and the verbatim text to find with Ctrl+F. Use this skill whenever the user asks for a document "with references", "con fuentes", "con citas APA/IEEE", "con hipervínculos en las citas", "con capturas de las fuentes", wants sources they can verify or screenshot, mentions instructor rules about allowed sources (e.g. no Wikipedia/ResearchGate, standards like NIST/ISO/IEEE, peer-reviewed articles, patents), or asks to add verifiable citations to a document they already wrote — even if they never say "CiteProof".
---

# CiteProof

CiteProof produces documents where **every citation can be proven**. Each citation in the text gets evidence next to it:

- **Auto mode:** Claude opens the source, highlights the exact passage and inserts a screenshot linked to the page.
- **Manual mode:** Claude leaves a short highlighted note saying *which citation* the evidence belongs to, a **clickable** link, and the verbatim fragment to search with Ctrl+F, so the user can take the screenshot in seconds.

The reason this matters: in academic work a citation is a promise that the source says what the text says. Students are increasingly asked to prove it (screenshots, "dynamic references"), and instructors reject sources that are not verifiable or recognizable. CiteProof turns that promise into checkable evidence and never lets a citation exist without a real, opened source behind it.

Reply to the user in their language. Write notes and captions in the document's language, but keep verbatim fragments in the **source's original language** — that is what Ctrl+F will find.

---

## Step 1 — Set up the job (once, briefly)

Before researching, settle four things. Ask in a single short message only for what the user hasn't already said; if they are not around to answer, use the defaults and state them at the top of your reply.

| Setting | Options | Default |
|---|---|---|
| Citation style | APA 7 · IEEE | APA 7 (IEEE if the field is engineering and the user hints at a paper/IEEE template) |
| Source rules | The user's/instructor's rules: banned sources, required source types, minimum counts, date range | Only the baseline policy (Step 2) |
| Evidence mode | `auto` (Claude takes screenshots) · `manual` (capture notes) · `both` | `auto` when a browser is usable, otherwise `manual` — decided per source |
| Output | .docx (default), Google Doc, Markdown, PDF…; language; length | .docx in the user's language |

Source rules belong to the user, not to this skill: record them exactly as given (e.g. "no ResearchGate", "definitions only from NIST, ANSI, ISO or IEEE", "include patents and the Gartner Magic Quadrant if it exists") and apply them throughout. If the user keeps a rules file or has stated rules earlier in the conversation, reuse them instead of asking again. Mention once that they can save their usual rules (for example in a `citeproof-rules.md` they attach or in their project instructions) so future documents start configured.

## Step 2 — Baseline source policy (always on)

Whatever the user's rules, every source must be:

1. **Verifiable** — it has a stable URL, DOI, standard number or patent number that anyone can open, and you actually opened it during this session.
2. **Veridical** — the text you attribute to it is really there (you copied the fragment from the page, not from memory), and it is current enough for the claim.
3. **Recognizable** — the author or publisher is identifiable and credible for that kind of claim (standards bodies, peer-reviewed journals, patent offices, governments and intergovernmental bodies, recognized analysts, the organizations that lead the technology, reputable press).

Read `references/source-policy.md` for the source tiers, red flags and how to swap a weak source (Wikipedia, ResearchGate copies, content farms, AI-generated pages, undated blogs) for the original. When a user rule is stricter than the baseline, the user rule wins; when a user rule would force an unverifiable source, explain the conflict instead of complying silently.

## Step 3 — Research and keep an evidence ledger

For every claim you plan to cite:

1. Open the source with your fetch/browse tools. Never cite a page you could not open.
2. Copy a **verbatim fragment** (roughly 8–25 words, unique on the page) that supports the claim. Short and distinctive beats long: Ctrl+F and the capture script both match it literally.
3. Record bibliographic data: author/organization, date (or *s.f.* / *n.d.*), title, publisher/site, URL or DOI, and source type (article, standard, patent, report, web page, press release).

Keep a running ledger while you work (a scratch table is fine):

`id | citation as it will appear | URL | verbatim fragment | type | opened? | notes`

If a source cannot be opened (paywall, blocked site, live dashboard), you may still use it only if the user supplied it or it is indispensable — and then mark it **UNVERIFIED** in the ledger, in its note, and in your final message. Numbers from live trackers (prices, market caps, user counts) get a note telling the user to capture the value on the day and update the text.

## Step 4 — Write the document

- Write the content first, then attach evidence. Keep it as long as the user asked — evidence notes are not an excuse to pad, and a request for "short" means short.
- Cite in the chosen style. Read `references/apa7.md` or `references/ieee.md` for in-text forms and reference-list formats by source type (standards, patents, press releases, same author/same year, no date, organizations as authors…).
- Every in-text citation must have exactly one reference-list entry and vice versa.
- Figures and images taken from sources get a numbered caption with the source cited ("Figure 2. … Source: Gartner (2025a)") and their own evidence note pointing to the page that publishes them.

## Step 5 — Evidence for each citation

Place the evidence **right after the paragraph (or table/figure caption) that contains the citation**. One piece of evidence per citation occurrence that a reader would need to verify; if the same source supports two different claims in different sections, give each its own evidence and say which section.

### Manual mode — the capture note

A capture note is a highlighted (yellow), underlined block that the user deletes after taking the screenshot. Use exactly this shape so it is always the same:

```
[NOTE – DELETE] Hyperlink goes on the citation (Lee, 2021) · Link: https://www.federalreserve.gov/...
Ctrl+F: «a unified, coherent product that encapsulates both the storage of digital value»
```

In Spanish:

```
[NOTA – BORRAR] Hipervínculo en la cita (Lee, 2021) · Link: https://www.federalreserve.gov/...
Ctrl+F: «a unified, coherent product that encapsulates both the storage of digital value»
```

Rules that make the note useful:

- **Line 1 names the exact citation as it appears in the text** — `(Gartner, 2025a)`, `Weber y Staples (2022)`, `[7]` — plus the section if the same citation appears more than once. That tells the user where to attach the hyperlink after pasting the screenshot.
- **The URL must be a real, clickable hyperlink** in the output format (in .docx use an actual hyperlink element, not plain text). Users open it with Ctrl+click; a plain-text URL silently breaks the workflow.
- Line 2 is the verbatim fragment in the source's language, inside « ». Add a short tip after a `·` only when needed ("page is in Japanese", "live data: update the figure", "PDF: page 12").
- Put one general note at the top of the document explaining the convention once (what the notes are, that they get deleted, and to search 4–5 consecutive words if the whole fragment isn't found).

### Auto mode — Claude takes the screenshot

When a browser is available (Playwright/Chromium in the sandbox, or a browser tool connected to the user's machine), capture the evidence yourself:

```bash
python scripts/capture.py --url "<URL>" --find "<verbatim fragment>" --out evidence/03_lee2021.png
```

The script loads the page, finds the fragment, highlights it, crops the surrounding passage and stamps the URL and capture date on the image. Exit codes: `0` captured, `2` fragment not found, `3` page could not load (blocked, paywall, network). Look at every PNG before inserting it — a cookie banner or login wall over the text is a failed capture.

Insert the image where the note would go, make the **image itself a hyperlink to the URL**, and add a one-line caption: `Evidence for (Lee, 2021) — captured 2026-10-24`. Then also hyperlink the in-text citation to the same URL (in .docx, wrap the citation run in a hyperlink).

Fall back to a manual capture note for that single source whenever capture fails (exit 2 or 3, PDF sources the browser can't render, pages behind the user's login, or the network is blocked in this environment). Mixed documents are normal; tell the user which ones still need a manual screenshot.

### Building the .docx

`scripts/docx_notes.js` (Node, `docx` package) exports helpers that already follow these rules: `captureNote()` for manual notes with a clickable link, `evidenceImage()` for a hyperlinked screenshot with caption, and `citedText()` for a paragraph whose citations are hyperlinked. Use them instead of rebuilding the formatting by hand. If you write the document another way, keep the same visual result: yellow highlight + underline, Arial ~10 pt for notes, URL as a real hyperlink.

## Step 6 — Reference list

Title it "Referencias"/"References" (APA) or "References" (IEEE). APA: alphabetical, hanging indent, same-author same-year disambiguated with a/b/c in both text and list. IEEE: numbered in order of first citation. Every URL in the list is a clickable hyperlink; prefer DOIs (`https://doi.org/...`) for articles.

## Step 7 — Check before delivering

Go through this list; fix problems rather than reporting them:

1. Every in-text citation has one reference entry, and every entry is cited.
2. Every citation has evidence (screenshot or note) and every note names its citation.
3. Every URL in notes and references is a working hyperlink element (for .docx, inspect `word/document.xml` for `w:hyperlink`).
4. No source violates the user's rules or the baseline policy.
5. Render the document (e.g. convert to PDF and look at the pages) to catch broken images, split tables and stray formatting.

## Step 8 — Deliver

Send the file and, in a few lines: the style and evidence mode used, how many citations got automatic screenshots vs. manual notes, and anything still pending (UNVERIFIED sources, live figures to update, sources the user's rules forced you to drop). Don't recap the research process.
