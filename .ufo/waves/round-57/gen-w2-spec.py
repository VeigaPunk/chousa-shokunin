#!/usr/bin/env python3
"""Generate the round-57 wave-2 spec (residual falsify wave, 8 seats). Writes w2-spec.json."""
import json
import pathlib

L = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
EV = f"{L}/corpus/evidence/round57"
SCR = "/fast/scratch/hyaku/chousa-r57"
FC2 = "c2f914c53201a8f8ee4fef823b82681051d55592"
FC3 = "fd95724d56a33a150cd2638fadd2ce1f3425e6c"
TIP = "1c9626efba2455d513b6b18df9b3df291e66556f"
W2 = f"{L}/.ufo/waves/round-57/w2"
GODSPEED = ("/skill:godspeed\n\nYou are a Godspeed-enabled subagent.\n\n1. **Name the axes.**\n"
            "2. **Iterate cheap, in parallel.**\n3. **Keep moves that improve any axis and harm none.**\n"
            "4. **Don't aim — let the frontier walk itself.**\n\nIMMEDIATELY STOP ASKING CLARIFYING "
            "QUESTIONS. Execute tool calls concurrently in large batches. Do not serialize what can "
            "run in parallel. Do not output philosophical reasoning or verbose plans. Act directly "
            "via tool calls.\n\n")

CONTEXT = f"""# Goal
chousa lane, round 57, residual falsify wave W2 (8 seats) against the LANDED claim state. Both claims have landed and are PASS at lane tip {TIP}: R57-C2 (`python3 {EV}/c2-count.py` → C2=PASS, receipt state at master `e0e73e0f`) and R57-C3 (`python3 {EV}/c3-count.py` → C3=PASS, manifest `{EV}/c3/`). Frozen claims: {EV}/claims.md (C2 freeze {FC2}, C3 freeze {FC3}). NEVER propose predicate/target/recipe changes; findings are reported, not patched. Wave-1 reports (65) are in {L}/.ufo/waves/round-57/w1/ — read the ones your item names.

# Boundaries (binding)
Lane repo: {L}. Your ONLY write is your own report file {W2}/<YourSeatName>.md. Never write any other lane file (a wave-1 seat dirtied corpus/evidence/round45/spans.tsv and was restored — that class of incident is exactly what this wave checks for), never the fleet root, never a sibling lane, never /home/vgpnk/Projects/shokuknow. Never run git/jj mutating commands except inside your own scratch fixture clone (`git clone --shared`, checkout inside the clone only). Frozen counters must never be edited; mutate copies in your scratch. Scratch ONLY under {SCR}/<YourSeatName>/ (mkdir -p; export TMPDIR=$PWD, PYTHONDONTWRITEBYTECODE=1; delete it before you yield). NO external network fetches.

# Evidence
Ground every statement in a command you ran; paste commands with observed output. A check you did not run has not passed. <=120 lines. End with a one-line VERDICT naming what you attacked and survives/falsified.

# Tooling
Tooling authorization (operator, 2026-10-19): you may install tools that help — read /home/vgpnk/.omp/agent/RULES.md first (official channels; record tool/version/channel/reason). pacman guard: ALL pacman transactions are PAUSED host-wide; use uv/npx/~/.local/bin. Routing is host-owned; never pass a model."""

items = []


def add(name, role, text):
    items.append({"name": name, "role": role,
                  "item": GODSPEED + text + f"\n\nReport: .ufo/waves/round-57/w2/{name}.md"})


add("R57W2MutC2Counter", "mutation-tester",
    "Mutation-test the frozen counter " + EV + "/c2-count.py at the AFTER-state (the live lane passes C2=PASS). "
    "In a scratch clone (`git clone --shared " + L + " $S/lane` — its working tree carries the landed state), apply one single-edit mutant at a time and run the copy's counter: "
    "M1 MIN_REPRODUCED 5→1; M2 drop the >=600s spacing rule; M3 drop the FLAGGED==need_flag term; M4 drop the CONSISTENT leg (count every backed capture consistent); M5 take the FIRST successful attempt instead of the last; M6 drop SET_N==47 enforcement; M7 count UNREACHABLE with only one failed attempt; M8 drop the txt_sha256 match inside CONSISTENT. "
    "Every mutant must print C2=PASS on the live state (a mutant that flips to FAIL is a counter-kill — report which leg it kills). For each mutant paste the summary line. Table mutant → PASS/FAIL → leg killed.")
add("R57W2MutC3Counter", "mutation-tester",
    "Mutation-test the frozen counter " + EV + "/c3-count.py at the AFTER-state (live lane passes C3=PASS). Scratch clone as in the C2 item. Single-edit mutants: "
    "M1 MIN_BOUND 4→3; M2 drop the heading_title leg from the binding rule; M3 drop the token-in-form leg; M4 drop the MIN_PER_ID>=2 manifest leg; M5 accept ANY registry row (drop the mined/held and EXCLUDED checks); M6 drop the STRAY_IDS leg; M7 drop ANCHOR_BOUND; M8 accept the first source-cell URL mismatch (skip the cites() regex). "
    "Every mutant must print C3=PASS on the live state; a FAIL is a kill — name the leg. Paste per-mutant summary lines.")
add("R57W2CritC3Forge", "critic",
    "Forge C3=PASS without genuine documents, in a scratch clone at the landed state. Attacks: "
    "(1) re-use the held S118 capture bytes for a SECOND row under a different id/URL — does good_raw[(id,url)] block it? "
    "(2) bind R4 by pointing a new row's URL at the catcm page (whose form mentions the R1 title but not the R4 title) — heading_title for the R4 title must fail; "
    "(3) write an entry whose quotes are all real but one manifest quote padded past 160 chars / 25 words — SHORT leg must fail; "
    "(4) an entry mentioning S130 in prose — STRAY_IDS must fail. For each: the exact counter output. Any attack reaching C3=PASS is a falsifier — report it first.")
add("R57W2ReviewC2After", "reviewer",
    "Final re-derivation of R57-C2 at HEAD: (1) `git -C " + L + " diff " + FC2 + " HEAD -- corpus/evidence/round57/claims.md corpus/evidence/round57/c2-count.py corpus/evidence/round57/controls` must be empty (paste); "
    "(2) run `python3 " + EV + "/c2-count.py` twice, paste both summary lines (both must be the after-receipt); "
    "(3) re-run the three controls via `python3 " + EV + "/controls/build-c2-controls.py $S/ctl` on a scratch clone and paste each profile; "
    "(4) run `python3 " + L + "/corpus/evidence/round55/wave-settled-check.py --round 57` (or read it and apply its rule manually) and confirm w1's results file is committed at or before the round-57 report will be; "
    "(5) verify `python3 " + L + "/tools/store-record-audit.py` exit and output at HEAD (expect FAIL on the two known record-denied classes — named, not a claim defect).")
add("R57W2ReviewC3After", "reviewer",
    "Final re-derivation of R57-C3 at HEAD: (1) run `PYTHONDONTWRITEBYTECODE=1 python3 " + L + "/tools/build-spans.py --check --quotes " + EV + "/c3/quotes.tsv --out " + EV + "/c3 --cache " + L + "/corpus/captures` (paste SPANS_ROWS/STALE); "
    "(2) independently re-verify each bound row's heading/token rule: for S131/S132/S133 open the committed .txt, whitespace-remove, confirm the title-as-heading line and the edition token, and confirm the capture bytes equal the last successful refetch row for (id,url); "
    "(3) run `python3 " + L + "/corpus/evidence/round51/quote-substance-check.py " + EV + "/c3/spans.tsv` and the c3 counter; paste outputs; "
    "(4) verify the frozen inputs: `git -C " + L + " diff " + FC3 + " HEAD -- corpus/evidence/round57/c3-count.py` empty.")
add("R57W2CritDoNothingRound", "critic",
    "Build the whole-round do-nothing control: a scratch clone checked out at the round base 6656f0770a1460d6ba73d9d2976f698a35311921 PLUS only the wrap-up capture bytes (git show b022b13:corpus/captures for the 14 files) and nothing else — no refetch.tsv, no entry, no manifest, no rows. Run both counters on the clone. "
    "Both must FAIL (C2: VERDICTS<47; C3: ENTRY=no). Paste both outputs. If either passes, the round's claims are reachable without the claimed work — report as falsified.")
add("R57W2SentFinal", "sentinel",
    "Final scope sweep at HEAD: (1) `git -C " + L + " status --porcelain` — classify every path (must be nothing, or only files this wave's seats add under .ufo/waves/round-57/w2/); "
    "(2) `find " + L + "/.ufo/waves/round-57 -type f | wc -l` and list any file outside w1/, w2/, and the four round-57 root files; "
    "(3) fleet-root check: `find /home/vgpnk/Projects/shokunin -maxdepth 1 -newer " + EV + "/claims.md` (paste; must show only lane-internal paths); "
    "(4) scratch audit: `ls /fast/scratch/hyaku/chousa-r57/` — every seat dir present names a live seat or a self-reported defect; list leftovers; "
    "(5) read `R57W1SimpRound.md` §6a and confirm corpus/evidence/round45/spans.tsv is clean at HEAD (`git diff --name-only HEAD -- corpus/evidence/round45/`).")
add("R57W2ReviewReport", "reviewer",
    "Pre-file contract check. Read /home/vgpnk/Projects/shokunin/.ufo/prompts/chousa-round-57.md §4 (report contract) and R57W1ReviewReportShape's checklist. Then read the L1's report draft at /home/vgpnk/Projects/shokunin/.ufo/reports/round-57/chousa.md if it exists by the time you run (if absent, check the w2 dir for a draft named chousa-report-draft.md and review that). "
    "Verify: required sections in order; the SHONEN grep gate; every measurement citation names the revision its receipt names (QUALITY 108); wave-settled before filing (w1 and w2 results committed); round shape/seat mix/dead seats stated; Sources & frontier has the census before/after with exit codes; trend verdicts one per trend; no universal clause without its counting command; Stale-lane line; tool installs recorded. List every gap as a defect or pass.")

spec = {
    "wave": "chousa-r57-w2",
    "milestone": "Round 57 wave 2 (chousa): residual falsify — mutate both frozen counters at the PASS state, forge C3, re-derive both receipts, do-nothing control, final scope sweep, pre-file contract check.",
    "axes": ["freshness", "depth", "calibration"],
    "reportDir": ".ufo/waves/round-57/w2",
    "context": CONTEXT,
    "items": items,
}
out = pathlib.Path(__file__).parent / "w2-spec.json"
out.write_text(json.dumps(spec, indent=1), encoding="utf-8")
from collections import Counter
print("items:", len(items), Counter(i["role"] for i in items))
