# R86CriticClaims — round-86 claim critic (L1 review seat)

Root `/home/vgpnk/Projects/shokunin/chousa-shokunin`. Revisions: base `3bfb6885…`, landing `667a5d09…`, live HEAD
`a9bed303…` (differs from landing only in three `.ufo/waves/round-86/` files — see "Provenance of the scored subject"
in the C1 section). Trees built with
`git archive <rev> | tar -x -C /fast/scratch/hyaku/chousa-r86/R86CriticClaims/{land,base}`. No network, no lane git
mutation, no production edit. Only files written: this report and `.ufo/waves/round-86/w1/R86CriticClaims/`
(receipts) inside my seat folder; every fixture lives in `/fast/scratch/hyaku/chousa-r86/R86CriticClaims/` and is
deleted before yield. No tool installed, no pacman transaction.

**Frozen bytes match the pins before any measurement** (both trees, all four files):

```
20bc1a73…  gate-records-r86.py   84a64ad4…  curation-r86.py
8c089828…  c2-positives.tsv      fe204539…  tools/gate-records.py
```

`land/tools/gate-records.py` == `base/tools/gate-records.py` == the pinned subject sha, so "subject tool unchanged
this round" holds.

Both frozen control receipts reproduce on the trees I extracted: base C2 `SUPERSEDED_LIVE=1 UNENTAILED_TERM=2
MODIFIED_DEF_CITED=0 QUOTES_LOCATED=19/19 FAIL exit 1`; the C1 do-nothing shape reproduces in the T1 row of the C1
table. Both landing
predicates reproduce exactly (receipts `c1-landing.txt`, `c2-counting-command-live.txt`).

---

## C1 — control (1), do-nothing C1

`corpus/evidence/round86/gate-records-r86.py --root land --repo <lane> [--tool X] --work <scratch>`.
All candidate tools are derived from the landed subject; only the named bytes differ.

| candidate | bytes | observed | exit |
|---|---|---|---|
| landed subject | — | `POSITIVE=15/15 FRESH_POSITIVE=5/5 FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 EMPTY_REFUSED=1/1 RC=4/4 SETUP=1/1 D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1` / `PASS` | 0 |
| **T1** one-token revert `r[6] == "200"` → `r[6].startswith("2")` | `t1.py` | `FORGED_REFUSED=354/355 EXPECTED_CODE=354/355 … D1_REFUSED=0/1 MUT17_KILLED=0/1` / `FAIL` (+`NOT_REFUSED g0354.md D1-203-admit S021`) | 1 |
| **T2** T1 + hard-coded refusal of the cookie-challenge body + a *dead* `r[6] == "200"` literal | `t2.py` | `FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 … D1_REFUSED=1/1 MUT17_KILLED=0/1` / `FAIL` (+`MUT17_NOT_RELAXED`) | 1 |
| **T4** `r[6] == "200" if sid == "S021" else r[6].startswith("2")` — general 2xx, one record-keyed exception | `t4.py` | `FORGED_REFUSED=355/355 EXPECTED_CODE=355/355 … D1_REFUSED=1/1 MUT17_KILLED=1/1` / **`PASS`** | **0** |
| **T3** semantically identical repair phrased `int(r[6]) == 200` | `t3.py` | `… D1_REFUSED=1/1 MUT17_KILLED=0/1` / `FAIL` | 1 |

Receipts: `R86CriticClaims/c1-{landing,t1-2xx-revert,t2-hardcoded-d1,t4-record-keyed,t3-rephrased-200}.txt`,
fixtures `fixture-t4.diff`.

**T1 is precise:** with the landing tree and only the 200-only rule reverted, *every* other leg passes
(15/15, 5/5, 354/355, 354/355, 1/1, 4/4, 1/1). The two round-86 legs are the sole discriminators — so the question
"can anything pass with D1_REFUSED=1/1 and MUT17_KILLED=1/1 without the repair" is exactly a question about those
two legs alone.

**T2 shows the mutant leg does its job.** A tool that fabricates `D1_REFUSED=1/1` from a hard-coded body string
cannot also make the derived mutant accept D1, because `mut_accepts_d1` is true only when the refusal is *caused*
at the `r[6] == "200"` site the mutation rewrites. A dead literal does not help. This leg is sound.

**T4 is the available counterexample, and it passes.** The predicate's only negative instance is S021. A rule that
applies `200` to S021 and `2xx` to everything else satisfies both legs: `D1_FORGES=1 D1_REFUSED=1/1
MUT17_KILLED=1/1`, exit 0. So the answer to control (1) is **yes**: a tool that does not carry the claimed general
repair passes the round-86 counter.

The missing leg is not missing — it is unused. Three committed refetch rows have `curl_rc=0` and `http=203`
(`S021`, `S032`, `S022`) and all three build a quotable admit with a matching capture sha
(`c1-d1-identity.txt`, `c1-second-d1-instance.txt`):

```
land/tools/gate-records.py on the S032 203 admit → GATE_RECORD d1b.md:1 S032 FAIL REFETCH   rc=1
t4.py                      on the S032 203 admit → GATE_RECORD d1b.md:1 S032 OK            rc=0
```

Building D1 from **all** qualifying rows and requiring `D1_REFUSED=N/N` (3 at landing) kills T4 and keeps the landed
tool green. `build_d1_203_admit` returns the first match only (line 280), so the class is one record wide where the
committed bytes support three.

**Fidelity of the D1 instance is not pinned either.** Prepending a 203 row for `S023` to a scratch refetch table
moves the built record to `S023` while the D1 legs still print `D1_FORGES=1 D1_REFUSED=1/1 MUT17_KILLED=1/1`
(`c1-d1-identity.txt`: `land -> S021`, `v5 -> S023`, `v8 -> S032`). C1's sentence names "the committed `S021`
PubMed refetch row"; the predicate `D1_FORGES=1` does not.

**T3 is a tradeoff, not a defect at this landing.** A correct tool whose rule reads `int(r[6]) == 200` scores
`MUT17_KILLED=0/1`, because `build_mutant` substitutes the literal text. K4 freezes exactly that outcome, and the
subject tool is pinned with one literal and no `sid` guard, so nothing here falsifies C1 — but the predicate scores a
byte pattern, not the capability, and the next revision that rephrases the rule will fail a correct tool.

**Provenance of the scored subject (recorded, not yet harmful).** `--tool` takes any path (lines 299/303) and the
counter never asserts the pinned subject sha, so a scorer who passes `--tool` scores a different subject; the frozen
counting command omits it, so the scored run is the landed tool. `--repo` names the live lane (HEAD `a9bed303`), not
the revision under test (`667a5d09`); the two differ only in `.ufo/waves/round-86/{build_spec.py,w1-dispatch.json,
w1-spec.json}`, so the fresh `rev=` positives (read by `git grep` against `--repo`) are byte-identical today, but the
run is not a function of the landing bytes alone.

---

## C2 — control (2), do-nothing C2

`curation-r86.py --root <tree>`; variants are copies of `land` (or `base`) with one edit, fixtures under
`R86CriticClaims/fixture-v*.diff`.

| variant | edit | observed | exit |
|---|---|---|---|
| landing | — | `SUPERSEDED_LIVE=0 UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20` / `PASS` | 0 |
| base | — | `1 / 2 / 0 / 19/19` / `FAIL` | 1 |
| **V1** | `S024` status `queued`→`mined` **and** its `used by` cell → `provenance-recording-r85.md` | `0 / 0 / 1 / 20/20` / **`PASS`** | **0** |
| V7 | `S031` row deleted | `0 / 0 / 1 / 19/20` / `FAIL` (Q7 unlocated) | 1 |
| **V3** | base tree, `supersedes S024 —` → `Supersedes S024 —` | `0 / 2 / 0 / 19/19` / `FAIL` — `SUPERSEDED_LIVE` 1→0 from capitalisation alone | 1 |

**The prescribed do-nothing edit does not fail.** Restoring `S024` to `mined` *and* re-crediting it to the r85 entry
(the round-85 inversion's live-citation half) leaves the counter at `SUPERSEDED_LIVE=0 … PASS`. The reason is the
predicate's own shape: it fires only when the superseded row is `mined` *and* the superseding row is not
(lines 93–99). Once `S031` is `mined`, `S024` may be `mined` and `used by` the same entry with no finding — and the
r85 entry's `source:` header still says `S031`, so the registry and the entry then contradict each other.

This is *disclosed* pre-freeze (plan repair 1 narrows the predicate to the "live-vs-unadopted" form), so it is not a
hidden regression — but the disclosed rationale is "legitimate legacy two-row histories" (`S073`/`S176`/`S200`/`S201`),
where the superseded and superseding rows are credited to **different** entries. V1 is the same-entry case, which that
rationale does not cover and the narrowing does not exclude. Deleting the row is caught (V7); re-mining it is not.

`V3` shows the relation is discovered from free text by a case-sensitive literal match
(`re.match(r"supersedes (S\d{3,}) —", teaches)`, line 96), so capitalisation, a double space or an en dash removes a
row from the check without touching the registry semantics.

**No pure-registry edit passes at base** without also fixing the entries: `UNENTAILED_TERM=2` and
`MODIFIED_DEF_CITED=0` survive every registry-only change I tried. The entry-side passes are the cosmetic ones below.

---

## C2 — control (3), quote floors

**Yes — deleting quotes is a pass, and moving two elsewhere is not even needed.** The predicate is
`quotes_total > 0 and quotes_located == quotes_total` (line 142); the published floor is never implemented.

| variant | edit | observed | exit |
|---|---|---|---|
| **V4** | Q1–Q5 deleted from the r84 entry | `0 / 0 / 1 / 15/15` / **`PASS`** | **0** |

`claims.md` C2 states the predicate as "`QUOTES_LOCATED` equal to its total with the total ≥ 19"; at 15 the frozen
prose says FAIL and the instrument says PASS. Two further escapes share the cause: a quote row that does not split
into exactly three cells (a `|` inside the quote) is dropped from *both* numerator and denominator, and duplicate
qids are never rejected.

**`MODIFIED_DEF_CITED` is not pinned to `S023` or to the r84 entry, and the Warrant column is never parsed.**
Line 128–130 counts the string in any located quote of *either* routed entry, with no `sid` and no `rel` test; no code
reads the `Warrant` cell at all.

| variant | edit | observed | exit |
|---|---|---|---|
| **V6** | Q13 removed from r84 → added to the r85 entry, tagged `S023`; r84 row 9 still reads `… Q13 (S023)` | `0 / 0 / 1 / 20/20` / **`PASS`** | **0** |

So "row 9 gains the `modified` Definition quote as its warrant" is not what is checked: an entry whose row 9 cites a
qid that no longer exists in that entry passes, because the sentence happens to be present in the sibling entry. This
is false provenance of exactly the kind C2 claims to close.

Not a counter defect, by the frozen wording: `UNENTAILED_TERM` is term presence, not entailment. `claims.md` puts
entailment in K3 (non-author reviewer), so a cosmetic cell rewrite that drops the word `modif*` without a new warrant
passes both the counter and the frozen predicate — the reviewer, not the instrument, is the control there.

---

## Impacted axes

- **operability (C1).** The predicate is met; the `D1` class is one record wide, so the battery certifies the claim's
  sentence without witnessing the general 200-only rule (T4 passes). The mutant derivation itself is sound (T2).
- **calibration (C2).** The predicate is met; the instrument is *weaker* than the published predicate (no `≥ 19`
  floor), the warrant leg is not tied to the row that needs it, and the supersession leg admits the superseded row
  re-mined and re-credited once the correction is mined.

## Smallest safe corrections (each keeps the landed tree green)

1. C2 predicate line 142: add `and quotes_total >= 19`; reject duplicate qids and rows that do not parse as three cells
   instead of dropping them.
2. C2 line 128: require `rel == ENTRIES[0] and sid == "S023"` for `MODIFIED_DEF_CITED`, and check that every decision
   row's `Warrant` qid exists in that entry's Located-quotes table.
3. C2 line 96: match the supersession prefix case-insensitively and tolerate dash variants; add "no entry's `source:`
   header cites a row that a later row supersedes" (this closes V1 without touching the legacy two-row histories).
4. C1 line 280/357: build D1 from every qualifying non-200 refetch row (`S021`, `S032`, `S022` at landing) and require
   `D1_REFUSED=N/N`; if the claim keeps naming `S021`, assert `d1_sid == "S021"`.
5. C1 line 303: assert `sha256(tool) == fe204539…` unless `--tool` is the labelled do-nothing control.

None of these is applied by me: the freeze is the authority and this seat is leaf.

---

## Receipts (path relative to the lane root; each file's header repeats the exact command and exit)

`.ufo/waves/round-86/w1/R86CriticClaims/` — `c1-landing.txt`, `c1-t1-2xx-revert.txt`, `c1-t2-hardcoded-d1.txt`,
`c1-t4-record-keyed.txt`, `c1-t3-rephrased-200.txt`, `c1-d1-identity.txt`, `c1-second-d1-instance.txt`,
`c2-counting-command-live.txt`, `c2-landing.txt`, `c2-base.txt`, `c2-v1-s024-remined.txt`, `c2-v3-capitalized.txt`,
`c2-v4-quotes-15.txt`, `c2-v6-q13-moved.txt`, `c2-v7-s031-deleted.txt`, and the fixture diffs
`fixture-{t4,v1,v3,v4,v6,v7}.diff`. Every tree is `git archive <rev> | tar -x` under
`/fast/scratch/hyaku/chousa-r86/R86CriticClaims/`; every variant is a `cp -a` of `land`/`base` plus the one diff shown.

## Verdicts

VERDICT: R86CriticClaims C1 held — the frozen predicate is met exactly at the landing revision (355/355,
D1_REFUSED=1/1, MUT17_KILLED=1/1, exit 0) and the mutant leg is sound, but the single-instance D1 class is passed by a
record-keyed 2xx tool (t4), so the claim certifies its sentence without witnessing the general 200-only rule.
VERDICT: R86CriticClaims C2 held — the frozen predicate is met exactly at landing (SUPERSEDED_LIVE=0
UNENTAILED_TERM=0 MODIFIED_DEF_CITED=1 QUOTES_LOCATED=20/20, exit 0), but the instrument implements a weaker
predicate than claims.md publishes (no `total ≥ 19` floor, 15/15 passes) and accepts the superseded row re-mined and
re-credited to the same entry.
