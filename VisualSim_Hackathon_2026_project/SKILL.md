---
name: missile-defense-paper-research
description: Deep, citation-grounded analysis of research papers on missile defense systems (BMD, IAMD, counter-UAS/cruise-missile defense, early warning, sensors and tracking, discrimination, interceptor guidance and control, C2/BMC3I, sensor fusion, engagement simulation, cost-exchange and architecture studies). Use this skill whenever the user provides, points to, or mentions research papers, PDFs, arXiv/IEEE/DTIC/technical-report files, a papers folder, or asks for a literature review, paper summary, comparison, critique, gap analysis, or synthesis in the missile defense domain, even if they just say "read these papers" or "go deep on this".
---

# Missile Defense Paper Research

Perform rigorous, evidence-grounded deep research on a set of provided papers. The goal is understanding, critique, and synthesis of what the papers say, not inventing claims beyond them.

## Scope

- Analyze, summarize, compare, critique, and synthesize the provided literature.
- Stay at the level of the papers' own content. Do not extend the work into new weapon designs, optimized attack strategies, or ways to defeat a defensive system. If the user asks for that, decline that part and offer analysis of the papers' stated findings instead.
- Note distribution/classification markings (e.g., "Distribution A", "CUI", "FOUO") if present, and mention them in the report.

## Ground rules

1. **Never fabricate.** Every claim must trace to a specific paper and location (section, page, figure, or table). If unsure, write "not stated in paper".
2. **Separate three things:** what the authors *claim*, what the authors *demonstrate* (evidence), and your own *interpretation*. Label each.
3. **Quote sparingly.** Paraphrase; use short quotes (under 15 words) only when exact wording matters.
4. **Record uncertainty.** Flag simulation-only results, unrealistic assumptions, synthetic or unreleased data, and missing baselines.
5. **Prefer reading the full paper** over relying on abstracts. Do not summarize from the abstract alone.

## Workflow

### Phase 0: Intake
1. List the paper files (PDF, md, txt, tex). Count them and note anything unreadable.
2. Extract text. Try in order: `pdftotext -layout file.pdf out.txt`, then `python -c "import pypdf"` / `pymupdf`, then OCR (`ocrmypdf` / `tesseract`) for scans. Check that equations, tables, and figure captions survived; note when they did not.
3. Create a working directory `research/` with:
   - `research/notes/<paper-id>.md` (one per paper)
   - `research/synthesis.md`
   - `research/report.md`
   - `research/open-questions.md`
4. Ask the user (once, briefly) for the research question or focus if none was given. If they don't answer, default to a general landscape analysis.

### Phase 1: Per-paper deep read
For each paper, write `research/notes/<paper-id>.md` using this template. When there are many papers and subagents are available, delegate one paper per subagent with this same template, then review every note yourself.

```
# <Title> (<Authors>, <Year>, <Venue/Report no.>)
- File: <path>   Markings: <if any>
## Problem & motivation
## Threat/mission context   (what is being defended against, in the paper's own framing)
## Defense layer / system element
   (early warning, sensing, tracking, discrimination, C2/BMC3I, fire control,
    interceptor guidance/propulsion, effects/kill assessment, architecture)
## Method / approach
   (models, algorithms, filters, optimization, learning, game theory, etc.)
## Assumptions   (list each; mark which are strong or unrealistic)
## Data / simulation setup   (real vs synthetic, scenarios, fidelity, tools, seeds)
## Metrics & results   (numbers with table/figure refs)
## Baselines & comparisons
## Claims vs. evidence   (table: claim | evidence | strength: strong/partial/weak)
## Limitations   (authors' stated + your identified)
## Reproducibility   (code/data available? parameters complete?)
## Key references worth chasing
## Quotable / page-anchored facts
```

### Phase 2: Domain lens
While reading, check each paper against the areas relevant to it:

- **Sensing & tracking:** sensor modalities (radar, IR/EO, space-based), track initiation, filtering (EKF/UKF/particle/IMM), data association, track-to-track fusion, handling of clutter, decoys, and maneuvering targets.
- **Discrimination & classification:** features used, classifier type, training data realism, false alarm/miss tradeoffs.
- **Guidance, navigation & control:** guidance law, autopilot/seeker models, maneuver and miss-distance analysis, robustness to model error.
- **Engagement & resource management:** weapon-target assignment, shoot-look-shoot policies, magazine depth, scheduling, sensor tasking.
- **C2/BMC3I & architecture:** latency, networking, interoperability, layering, cost-exchange ratio, saturation behavior.
- **Evaluation:** probability of kill/engagement success, detection and false-alarm rates, Monte Carlo size and confidence intervals, sensitivity analysis, validation against test data.
- **Methodological red flags:** perfect-information assumptions, ignoring sensor noise or latency, single scenario, tuned on test set, no comparison to a classical baseline, unclear units/coordinate frames, results not reproducible from the text.

Only note the dimensions that apply; do not pad.

### Phase 3: Cross-paper synthesis (`research/synthesis.md`)
- **Taxonomy:** group papers by problem, defense layer, and method family.
- **Comparison matrix:** rows = papers; columns = problem, method, data/fidelity, key metric, main limitation. Keep metric comparisons honest: only compare numbers produced under comparable assumptions, and say when they aren't.
- **Agreements and contradictions** between papers, with citations on both sides.
- **Evolution:** how approaches changed over time, and which ideas recur.
- **Evidence strength map:** which conclusions are well supported across multiple papers and which rest on one simulation.
- **Gaps:** untested assumptions, missing validation, under-studied regimes, missing baselines.

### Phase 4: Verification pass
Before writing the final report:
1. Re-open the source for every number, equation, and strong claim you plan to cite and confirm it.
2. Remove or soften anything you cannot re-confirm.
3. Check that citations point to the right paper and location.
4. If a claim in one paper depends on a cited paper that is not in the set, say so and mark it as unverified.

### Phase 5: Report (`research/report.md`)
Structure:
1. **Executive summary** (max ~250 words): the most important findings and the confidence in them.
2. **Scope & corpus:** papers covered, anything unreadable, markings.
3. **Landscape overview:** taxonomy and trends.
4. **Detailed findings** by theme, each with citations like `[P3, §4.2, Fig. 7]`.
5. **Comparison matrix.**
6. **Critical assessment:** strengths, weaknesses, validity threats.
7. **Gaps & open questions** (also write to `research/open-questions.md`).
8. **Suggested further reading** (only things referenced in the papers or clearly identified; no invented citations).
9. **Bibliography** with the paper IDs used throughout.

Write in plain, precise language. Define acronyms on first use. Use tables for comparisons, prose for reasoning.

## Handling requests

- **"Summarize paper X":** do Phase 0-1 for that paper only and give a concise summary plus the claims-vs-evidence table.
- **"Compare these papers":** Phases 0-3, focus on the matrix and contradictions.
- **"Find gaps / what's missing":** Phases 0-3 with emphasis on limitations and untested assumptions.
- **"Explain the math":** reconstruct the derivation step by step from the paper, state each assumption, and flag any step the paper skips.
- **Follow-up questions:** answer from the existing notes first; re-open the source only if the notes don't cover it.

## If something goes wrong
- Unreadable PDF or garbled equations: say so, describe what is lost, and ask whether the user can provide another format or the LaTeX source.
- Paper outside the missile defense domain: process it with the same template and note the mismatch.
- Very large corpus: process in batches, keep notes per paper, and synthesize from the notes rather than re-reading everything.
