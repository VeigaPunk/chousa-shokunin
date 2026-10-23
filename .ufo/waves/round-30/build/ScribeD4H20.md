# Scribe D4 h20 — findings
- **Behavior:** drafted an append-only correction for the round-25 Gate line 70; no production file changed.
- **Finding:** ScoutFreshnessH line 89 says h20 is ABSENT because the quote changed “However, a signal” to “A signal”; corrected quote: “However, a signal occurred within 2 years for 23% of reviews and within 1 year for 15%.” (17 words; PubMed URL opened 2026-10-23, reader returned abstract via NCBI E-utilities; HTTP status not exposed).
- **Decision:** meaning change: no; quote fidelity only. Existing S021 admission remains queued (`SOURCES.md:31`); S032 supersedes S021 and is also queued (`SOURCES.md:42`).
- **Gates:** C1/C2 counters and other tests were not run; no claim about their results.
- **Touched surfaces:** only this report and `ScribeD4H20/correction.md` under the round-30 build directory. Out of scope: editing `lessons/round-25.md`, re-adjudicating admission, or changing source rows.
- **Evidence opened:** `corpus/lessons/round-25.md:70`; `.ufo/waves/round-29/falsify/ScoutFreshnessH.md:89`; `corpus/SOURCES.md:31,42`; PubMed URL above, once.
- **Command:** `timeout 10s mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-30/build/ScribeD4H20` — no output; call succeeded (exit status not separately shown). No tools installed or updated.
- **Artifacts:** `.ufo/waves/round-30/build/ScribeD4H20/correction.md`; `.ufo/waves/round-30/build/ScribeD4H20.md`.
