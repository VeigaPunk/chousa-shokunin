# Round 62 — claims erratum (appended after the freeze; the frozen `claims.md` is not edited)

`corpus/evidence/round62/claims.md` (sha256 prefix `a3193ebd328919e2`, freeze commit `388d153519a36a4c3f34d56d034870f032865a70`)
stays as frozen. Wave seat `CritCalibration` read it against the files after the freeze and found 14 statements its own
files contradict (`.ufo/waves/round-62/w1/CritCalibration.md`); the L1 re-checked each by the command shown. No predicate,
counter, kill rule or target changes; the measured verdicts rest on the counters, not on these sentences.
Line numbers are lines of the frozen `claims.md`.

| # | frozen text (line) | what the files show | corrected statement |
|---|---|---|---|
| 1 | "64 seats" (128) | `python3 -c "import json;print(len(json.load(open('.ufo/waves/round-62/w1-spec.json'))['items']))"` → 66; dispatch `counts` spawn 66 | one v2 wave of 66 seats; attack roles (reviewer 16, critic 11, mutation-tester 6) 33/66 |
| 2 | "attack share at least 25 %" (128) | undefined without naming the roles | reviewer, critic and mutation-tester count as attack roles: 33 of 66 |
| 3 | "routed defects 1 and 2" of `round-61-verifier-spotcheck.md` (11) | its item 2 is the `research-gate.sh --selftest` commit, not C1 | the C1 reason is `corpus/lessons/round-61.md` `## Mistakes` rows 1–2 and the closure's routed item 1 only |
| 4 | "the sentence in the docstring of c1v2-battery.py" (24) | the docstring is a longer text that cites claims.md as "the same sentence" (circular); the counter docstring carries a different label (R62-C1K) | the predicate is the paragraph of claims.md C1 above the counting command; both docstrings quote it in longer form |
| 5 | "the sentence in the docstring of c2v2-count.py" (87) | the docstring says "the same sentence as claims.md" and lists ENTRY, which the claim's list omits | same: claims.md C2 is the predicate; the docstring is the executable form |
| 6 | "14/14 facts" (92) | the counter enforces `PROBE_FACTS=k/k` and equality with the committed file, not 14 | `PROBE_FACTS=k/k` (14 at the candidate and at the landed probe) |
| 7 | "FORGERS_REJECTED=0/12 … all twelve forgers read 20/20" as a stable before (40–42) | F12 is a race: on one re-run of the same command `FORGERS_REJECTED=1/12` (F12 `LEGS=19/20`); eleven forgers read 20/20 | `0/12` in `controls/c1v2-before.txt` and `1/12` on one re-run; eleven forgers are accepted at every run seen |
| 8 | "`null-pass.py` … accepts 0/12 forgers and 0/4 stubs" (57) | `controls/null-counters.txt`: `FORGERS_REJECTED=0/12 STUBS_REJECTED=0/4` — it rejects none | `null-pass.py` rejects 0/12 forgers and 0/4 stubs (accepts all) |
| 9 | "a target no do-nothing counter reaches: the best do-nothing scores 12/12 only by rejecting the landing builder" (63) | only three do-nothing counters were run | none of the three do-nothing counters (`null-pass.py`, `null-fail.py`, `null-hashlist.py`) reaches `BATTERY=PASS`; `null-fail.py` and `null-hashlist.py` read `FORGERS_REJECTED=12/12` only by rejecting `LANDED` 0/3 |
| 10 | "each mutation that removes one profile feature or the sandbox lets exactly the forgers that feature stops through" (60–61) | X12 relaxes the both-profiles rule and lets the nine X01 forgers through; there is no X09 or X11 | X01–X08 each remove one profile feature or the sandbox; X12 relaxes the pairing; X10 survives |
| 11 | "under a 200 MiB address-space limit" (53) and the counter docstring | plain exactly 200 MiB; neutral 200 + randrange(0, 25) MiB | 200 MiB (plain) or 200–224 MiB (neutral) |
| 12 | "the builder cannot see the counter" (52) | the namespace hides the counter's process and its ancestors; the counter's files are readable and writable by the builder (`CritC1Sandbox`, `CritC1Detached`) | the builder cannot see the counter's process or ancestors; the sandbox is not a filesystem sandbox |
| 13 | "S138 is the lead recorded in `## Leads` by round 61" (85) | the lead was an unnumbered bullet; S138 is the id the row took in round 62 | the `openat2(2)` bullet under `## Leads (unopened)` is the lead; S138 is its row |
| 14 | "Round 61's recorded limit 'an echoing claim reaches PASS' is closed in v2" (108) | closed for the `echo-claim` control only; an echo with four filler words passes ECHO (`CritC2V2Forge` F1) | closed for the `echo-claim` control; ECHO is a three-fresh-word screen, not a proof |

Further corrections, not counted above: "four independently written correct builders" (27) — three are independent, `pos-ref` is the
round-61 reference; "into 20 fresh fixture directories" (counter docstring) — 18 fixture runs per profile carry the 20 legs;
the battery docstring says a counter "can read" nothing about the subject, but `RevQualityA` finding 4 shows a counter that keys on the
subject directory name (`F01`..`F12`) passes the battery — a hole in the frozen battery, routed; `claims.md` "the lane's only
scored axis" (C1) stays true for the numeric scale (operability 3/10) but the round also targets coverage (C2).

Digest prefix written in this file: `claims.md` `a3193ebd328919e2` (`sha256sum corpus/evidence/round62/claims.md | cut -c1-16`).
