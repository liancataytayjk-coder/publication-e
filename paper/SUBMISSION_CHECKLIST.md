# Submission checklist — "Approaching but Not Quite"

What remains before the manuscript can be submitted. Items marked **[author]** need the author's input.

## Must do

- [ ] **[author] Target journal.** Choose the journal (Q8 in `CLAUDE.md`). Candidate fits: *Asian Economic Journal*, *Journal of Asian Economics*, *The Philippine Review of Economics*, *Economic Modelling*, *Journal of Economic Studies*. Then apply its format: word limit (the draft has about 5,600 words of text before references, tables and figures), abstract limit (the draft abstract is about 260 words — trim if the limit is 150–250), reference style, title page, and whether tables/figures go at the end (they do now).
- [ ] **[author] Author block.** Replace `[Author name], [Affiliation], [email]` in `paper/manuscript_template.md`, then run `python scripts/08_paper.py`.
- [ ] **[author] Declarations.** Funding, competing interests, and the journal's AI-use statement (placeholders in the template).
- [ ] **Barro (2015) targets.** The replication targets were typed from NBER WP 18295 (2012). If you have access to the *Economic Journal* version, check Table 1, columns 1–4, against `replication/barro2015_targets.csv` (Q9).
- [ ] **V-Dem citation.** `vdem2025` in `paper/references.bib` is a dataset entry not indexed by Crossref. Replace with the full V-Dem citation (Coppedge et al., V-Dem Country-Year Dataset, version used by Our World in Data at download, 2026-10-15) and the V-Dem methodology reference.
- [ ] **Cover letter**: one paragraph on the question, the two-design approach, and the main finding (moving steady state; methods agree on speed, disagree on level until current demography is used).
- [ ] **Data statement**: all data public; replication package = this repository (`run_all.sh`).

## Should do

- [ ] Read the rendered `paper/manuscript.docx` once end to end for flow; edit `paper/manuscript_template.md`, never the rendered files.
- [ ] Decide whether to keep Table 8 (full coefficients) in the body or move it to an online appendix.
- [ ] Consider extending to 2024–25 with PSA national accounts (PWT ends 2023) — Q5.

## Already done

- [x] Replication gate pre-registered and passed (17/17); `output/tables/replication_gate.csv`.
- [x] Estimation plan pre-registered before any new-data estimate; post-run correction D13 and supplementary analyses D14 labelled in the text.
- [x] Every reference except V-Dem verified on Crossref (`scripts/crossref_check.py`).
- [x] Figures black and white, no in-image titles, 300-dpi PNG/TIFF + PDF.
- [x] No number typed by hand: all numbers come from `output/tables/paper_numbers.json`.
