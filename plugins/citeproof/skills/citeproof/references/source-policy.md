# Source policy

The baseline every source must pass is **verifiable, veridical, recognizable** (see SKILL.md, Step 2). This file helps you judge sources quickly and replace weak ones with the original.

## Tiers (prefer higher tiers for definitions and key claims)

| Tier | Source type | Examples | Good for |
|---|---|---|---|
| 1 | Standards and standards bodies | ISO, IEC, IEEE, NIST, ANSI (and ANSI-accredited committees such as ASC X9), ITU, W3C, IETF RFCs, ICONTEC | Definitions, terminology, technical requirements |
| 1 | Peer-reviewed literature | Journal articles and reviews with DOI (Elsevier, Springer, IEEE Xplore, ACM, MDPI, Wiley, Taylor & Francis); conference proceedings | Evidence, methods, findings |
| 1 | Patents | Google Patents, USPTO, EPO Espacenet, WIPO Patentscope | Who is building what; technical novelty |
| 1 | Official bodies | Governments, laws, central banks, BIS, IMF, World Bank, OECD, UN agencies, national statistics offices | Figures, regulation, policy |
| 2 | Recognized analysts | Gartner, IDC, Forrester, McKinsey Global Institute (public pages, press releases, report abstracts) | Market position, Hype Cycles, Magic Quadrants |
| 2 | Technology leaders | Official docs, white papers and newsroom of the organizations that lead the field | What the technology does in practice |
| 2 | Working papers from recognized institutions | Central bank staff papers, NBER, university labs (MIT, Stanford…) | Recent research not yet peer-reviewed — say so |
| 3 | Reputable press and trade media | Major newspapers, specialized trade outlets with named authors | Recent events, local context |
| ✗ | Avoid as a citation | Wikipedia, ResearchGate/Academia.edu copies, content farms, SEO listicles, AI-generated pages, undated or anonymous blogs, forums | Use only as leads to find the original |

## Replacing weak sources

- **Wikipedia** → follow its footnotes to the original source and cite that.
- **ResearchGate / Academia.edu** → these host copies. Find the publisher's page or DOI (search the exact title) and cite the publisher. If the work only exists there (an unpublished preprint), tell the user and let them decide.
- **Paywalled article** → cite the publisher page with DOI and capture the abstract; if the claim needs the full text, use an open version (arXiv, institutional repository, PubMed Central) and cite the published version.
- **Analyst reports behind paywalls (Gartner etc.)** → cite the free press release or the document's public abstract page, and capture that.
- **Secondary news about a study** → cite the study itself when you can open it.

## Quick verification checklist

1. Who published it, and are they credible for *this* claim?
2. Is there a date? Is it recent enough for the claim (market numbers, laws and rankings go stale quickly)?
3. Does the page say exactly what you will attribute to it? Copy the fragment from the page.
4. For journals, check the DOI resolves and, if the user asks for indexed or ranked journals (Scopus, Web of Science, "Q1–Q4"), verify the quartile in SCImago (SJR) or JCR instead of assuming it.
5. For figures and images, cite the page that publishes them, not an image search result.

## User rules

Apply the user's or instructor's rules on top of this policy exactly as stated, for example:

- "No ResearchGate" / "no Wikipedia" → never cite them, even as secondary.
- "Definitions from NIST, ANSI, ISO or IEEE" → definitions section must cite at least one of these; if none defines the exact term, say so and define it from the components they do standardize.
- "Include patents / standards / Magic Quadrant" → include them, and if one genuinely doesn't exist (e.g. no Magic Quadrant for an emerging technology), state that you searched and found none, and offer the closest alternative.
- Minimum counts or date ranges → track them in the ledger and confirm in the final message.
