# chain-r3.md / chain-r3-broken.md — pre-registered chain-hop fixtures (chousa round 3)

Round-3 coverage move (dispatch 2026-10-15): the round-1 gate checks chain hops
STRUCTURALLY only — a hop marked `resolved` passes `verify` as long as its `to`
resolves as a pointer; the anchor it cites is never looked for. These fixtures
pre-register, as fixed local inputs with fixed expected outputs, the new
`verify-chain` mode's job: every resolved hop's citation must resolve (source
under the corpus boundary + anchor bytes present in the target).

The record is the fixture. `chain-r3.md` is the positive control (22 real hops
over the three archived inputs, 17 resolved, 5 exempt — expected
`RESOLVED_HOPS=17/22`, CLEAN, exit 0). `chain-r3-broken.md` is the tampered
control: the same kind of hop, but it CLAIMS `status=resolved` while citing
anchor bytes the target does not carry — expected `RESOLVED_HOPS=1/2`, DRIFT,
exit 1.

## Authoring state

Lane HEAD `0aa794db58c2aafae0a50b25b8ae9822f4007900`; the fixtures are
uncommitted (`?? corpus/fixtures/chain-r3*.md`); no commits by this seat.
`verify-chain` did not exist at the round-2 revision (gate sha256
`03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`);
the implementation landed during this wave and the gate sha was observed
moving while it was written (`2c20d955…`, `ccfd1e5c…`, `6be40a7f…`,
`7379b7ee…`). Runs taken while the file was still being written are not
acceptance — the pinned revision is the settled sample in "Execution record".

The dispatch named `chain-r3.jsonl`; the landed mode reads Markdown records
(`tools/research-gate.sh:1033-1157`, `chain_citation`/`chain_anchor_at`), so the
fixture is the record `chain-r3.md` and the JSONL pre-draft was superseded and
removed rather than kept as a second, drift-prone copy of the same hops.

## Cited sources (pinned, read-only)

The three archived deep-research exports under
`research/deep-research-2026-09-28/` (fleet root, read-only), pinned to fleet
commit `0863746e9da95457f71b9e00a40361b88ab0df15`; sha256 re-derived
2026-10-15 and matching LOG.md:105-108:

```text
9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85  A-shokunin-tradition.md
6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006  B-multiagent-knowledge.md
e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b  C-rank-taxonomy.md
```

`pointer` cells are fleet-root-relative; the re-run passes `--root ..` from the
lane cwd (the round-1 convention). Every path resolves under the allowed local
corpus boundary (`research/deep-research-2026-09-28/`); no external fetch, no
URL source is opened, no session path. The two external hops (18, 19) are
pre-marked `blocked-no-fetch` and are cited as the exports' own chips
(コトバンク, arxiv.org): exempt and counted, never fetched.

## Hops — provenance and expected resolution

`from` is the citing locator inside the archived input (the line that makes the
chain), using the round-2 convention: `A:` = `A-shokunin-tradition.md`, `B:` =
`B-multiagent-knowledge.md`, `C:` = `C-rank-taxonomy.md`, and `S1`/`S2`/`S3` in
the `to` column are the record's own source ids for those three files (pinned
above, same order). The anchor bytes are the `anchor` cells of `chain-r3.md`
itself. "at" is the target's first-occurrence line, informational: the mode
verifies anchor EXISTENCE, not line binding or uniqueness.

| hop | from | to | kind | expected at | status | role in the method |
|---:|---|---|---|---:|---|---|
| 1 | A:35 | S1 | line | A:74 | resolved | question item (1) → the numbered section title answering it |
| 2 | A:47 | S1 | quote | A:64 | resolved | preamble finding → its evidence row |
| 3 | A:52 | S1 | quote | A:35 | resolved | negated ladder notation → the user's own term list |
| 4 | A:47 | S3 | line | C:107 | resolved | cross-input co-anchor of the jin'i-ryū negative finding |
| 5 | A:64 | S3 | quote | C:109 | resolved | cross-input co-anchor, failed-substantiation wording |
| 6 | A:54 | S2 | quote | B:57 | resolved | cross-input co-anchor, separate-the-axes move (A: four, B: five) |
| 7 | B:64 | S2 | quote | B:71 | resolved | table rows → the record's own Sources line |
| 8 | B:47 | S2 | quote | B:67 | resolved | closest-match finding → the Dynamic Cheatsheet/ACE row |
| 9 | B:47 | S2 | quote | B:79 | resolved | destructive-compression finding → the ACE evidence line |
| 10 | B:57 | S1 | quote | A:88 | resolved | cross-input co-anchor, evidence over declaration |
| 11 | B:57 | S3 | quote | C:67 | resolved | cross-input co-anchor, separate-the-axes move (B: five, C: four) |
| 12 | C:65 | S3 | line | C:87 | resolved | no-four-rank-ladder finding → its section title |
| 13 | C:87 | S3 | quote | C:89 | resolved | grading-structure title → its Go body line |
| 14 | C:65 | S1 | quote | A:52 | resolved | cross-input co-anchor, no universal ladder |
| 15 | C:75 | S1 | quote | A:63 | resolved | cross-input co-anchor, shokunin as occupational identity |
| 16 | C:65 | S2 | quote | B:55 | resolved | cross-input co-anchor, the create→…→agent-producing ladder not established |
| 17 | C:53 | S3 | line | C:107 | resolved | intra-C: preamble negation → its own section title (same anchor as hop 4) |
| 18 | A:67 | https://kotobank.jp/ | - | - | blocked-no-fetch | dictionary attestation outside the boundary; exempt, never fetched |
| 19 | B:71 | https://arxiv.org/ | - | - | blocked-no-fetch | the five cited papers outside the boundary; exempt, never fetched |
| 20 | A:64 | S3 | quote | - | unresolved | real chain break: 人為 is anchored only for jin'i (C:118), never for the coined rank |
| 21 | B:35 | S2 | line | - | unresolved | real chain break: question item (2) has no title line |
| 22 | C:69 | S1 | quote | - | unresolved | real chain break: C's recommended adaptation has no A-side anchor |

Ground truth for `chain-r3.md`: 22 hops read, 17 verified, 5 exempt,
0 anchor-missing/refused/invalid, 0 findings, `RESOLVED_HOPS=17/22`,
`RESEARCH_GATE: CLEAN`, exit 0.

Ground truth for `chain-r3-broken.md`: 2 hops read, 1 verified, 0 exempt,
1 anchor-missing, 1 finding, `RESOLVED_HOPS=1/2`,
`RESEARCH_GATE: DRIFT`, exit 1, with `FINDING CHAIN_ANCHOR_NOT_FOUND` on hop 2
(quote-kind miss with `nearest_line`/`context` reported).

## Why the negative control is the round's falsification

`chain-r3-broken.md` hop 2 claims `status=resolved` and cites, in export C,
`人為 — jin’i-ryū`. Export C carries `人為 — jin’i` (C:118) but never the coined
rank with that spelling, so the citation does not exist. That is exactly the
pre-move hole: round-1 `verify` passes this record CLEAN because `to=S3`
resolves structurally; `verify-chain` reports the hop `anchor-missing` and
drifts. The same bytes appear as the exempt hop 20 of `chain-r3.md`, so the
pair also shows the exemption rule: a real break stays counted and CLEAN only
when the record MARKS it (`unresolved` with a reason) instead of claiming it
resolved.

## Honest boundaries

- The three exports are independent chat sessions and do not cite each other;
  none of their bytes names another export. Cross-input entries (4, 5, 6, 10,
  11, 14, 15, 16) are therefore **co-anchor hops**: they pre-register only that
  the anchor bytes exist in the target input, never that the target input cites
  or endorses the source input. The relation the mode tests is anchor
  existence, not authorship.
- No export contains a Markdown heading: `grep -c '^#'` is 0 for A, B and C.
  The section-title anchors therefore use the `line` kind (one whole line,
  trailing whitespace trimmed) — the operative whole-line form on these inputs.
  A `heading`-kind anchor is impossible here by construction; that kind is
  exercised by the gate's own selftest cases on generated records.
- Anchors are byte controls, not adopted knowledge. Hop 9's numerals
  (18,282 / 122) are the round-2 boundary case (`claims-r2.README.md`,
  "Boundary"): reproduced only because digit-level byte fidelity is where
  citation resolution matters; nothing in this fixture is domain knowledge, and
  a CLEAN run verifies anchor identity, not the exports' own assertions.
- Exempt is not verified: hops 18-22 count but prove nothing about their
  citations. Hops 20-22 are deliberately included as real breaks the record
  marks instead of hiding as structural `resolved`s.
- The mode verifies existence, not semantics: hop 6 (four axes vs five) and
  hops 4/14 (two inputs agreeing in different words) resolve the anchor but say
  nothing about agreement.
- Text files only, read whole into memory after the same canonicalization and
  boundary checks as `verify-claims`; zero network.

## Execution record — 2026-10-15

Settled revision: gate sha256
`67daf85ecc49c4c7accbee9534c31b0734061b7f329e8de7a98254a57f9d6084`
(observed identical across four samples spanning ~90 seconds, after the gate
sha had moved through `7379b7ee…` and `1964ae03…` while the mode was being
written), lane HEAD `0aa794d`, fixture shas:

```text
06115f2f8e6db3c60034411dc6be42c4e0887352b09ab9cbd7f760801237ba07  chain-r3.md
b66222a16d4c5323ee6932839ff5746af5f716f36372af506755aed18e0f5c6a  chain-r3-broken.md
```

Rows sampled while the implementation was still being written are not results;
every command below was run at the settled sha, which is identical before,
between and after the runs.

1. `bash tools/research-gate.sh --selftest` →
   `RESEARCH_GATE_SELFTEST: PASS (40 cases)`, exit 0 (the 30 round-2 cases plus
   10 chain cases; `chain-fail-*`, `setup-chain-*` visible in the tail).
2. `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..`
   →
   `RESOLVED_HOPS=17/22`, 17 × `CHAIN … verdict=match` with gate-reported
   `at=` = 74, 64, 35, 107, 109, 57, 71, 67, 79, 88, 67, 87, 89, 52, 63, 55,
   107 — all agreeing with the provenance table above — then verbatim:

   ```text
   RESOLVED_HOPS=17/22
   RESEARCH_GATE: CLEAN (hops=22 verified=17 exempt=5 anchor-missing=0 refused=0 invalid=0 findings=0 drift=0)
   exit 0
   ```
3. `bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..`
   → verbatim:

   ```text
   CHAIN hop=1 status=resolved observed=verified source=research/deep-research-2026-09-28/A-shokunin-tradition.md anchor=quote:"I could not substantiate this spelling as an established art" at=line:64 verdict=match
   CHAIN hop=2 status=resolved observed=anchor-missing source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" at=- verdict=mismatch
   FINDING CHAIN_ANCHOR_NOT_FOUND severity=warn surface=chain obs=hop=2 source=research/deep-research-2026-09-28/C-rank-taxonomy.md anchor=quote:"人為 — jin’i-ryū" nearest_line=53 context=The key distinction is between skill, teaching authority, and permission to act.
   RESOLVED_HOPS=1/2
   RESEARCH_GATE: DRIFT (hops=2 verified=1 exempt=0 anchor-missing=1 refused=0 invalid=0 findings=1 drift=1)
   exit 1
   ```
4. The "before" side of the move, same revision: round-1
   `bash tools/research-gate.sh verify corpus/fixtures/chain-r3-broken.md --root ..`
   → `RESEARCH_GATE: CLEAN (findings=0 drift=0 questions=1 sources=2 chains=2 claims=1 negatives=0 rejections=1 approvals=1)`, exit 0 — the hop citing a
   non-existent anchor passes the structural check. `verify` on `chain-r3.md`
   is likewise CLEAN (22 chains), so each record is well-formed under both
   modes and the new mode's verdict is the only difference.
5. Round-2 regression at the same revision:
   `bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..`
   → `VERDICT_BEARING_CLAIMS=17/17`,
   `RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)`,
   exit 0 — `verify-claims` is unchanged by the chain mode.
6. Independent check, without the gate (the python below, run by this seat):

   ```text
   corpus/fixtures/chain-r3.md: RESOLVED_HOPS=17/22 bad_hops=[]
   corpus/fixtures/chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']
   ```

## Re-run

From the lane cwd:

```bash
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3.md --root ..
# expected: RESOLVED_HOPS=17/22; CLEAN (hops=22 verified=17 exempt=5
# anchor-missing=0 refused=0 invalid=0 findings=0 drift=0); exit 0
bash tools/research-gate.sh verify-chain corpus/fixtures/chain-r3-broken.md --root ..
# expected: RESOLVED_HOPS=1/2; DRIFT (... anchor-missing=1 ...); exit 1
bash tools/research-gate.sh verify corpus/fixtures/chain-r3-broken.md --root ..
# expected (round-1 hole): CLEAN, exit 0 — the structural check cannot see the miss
```

Independent byte-check without the gate (run now; expected output
`chain-r3.md: RESOLVED_HOPS=17/22 bad_hops=[]` and
`chain-r3-broken.md: RESOLVED_HOPS=1/2 bad_hops=['2']`):

```bash
python3 - <<'PY'
import pathlib
lane = pathlib.Path.cwd(); fleet = lane.parent
def table(path, want):
    sec, header, rows = None, None, []
    for line in open(path, encoding="utf-8"):
        if line.startswith("## "): sec = line[3:].strip(); continue
        if sec != want or not line.lstrip().startswith("|"): continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None: header = cells; continue
        if set(cells[0]) <= set("-: "): continue
        rows.append(dict(zip(header, cells)))
    return rows
def run(path):
    src = {r["id"]: r["pointer"] for r in table(path, "Sources")}
    n = ver = 0; bad = []
    for r in table(path, "Chain"):
        n += 1
        if r["status"] != "resolved": continue
        ref = src[r["to"]] if r["to"] in src else r["to"]
        ref = ref.split(":")[0].strip("`")
        hay = (fleet / ref).read_text(encoding="utf-8")
        kind, a = r.get("anchor_kind", ""), r.get("anchor", "")
        if kind == "line":
            ok = any(l.rstrip() == a for l in hay.splitlines())
        elif kind == "quote":
            ok = a in hay
        else:
            ok = False
        if ok: ver += 1
        else: bad.append(r["hop"])
    print(f"{path}: RESOLVED_HOPS={ver}/{n} bad_hops={bad}")
run("corpus/fixtures/chain-r3.md")
run("corpus/fixtures/chain-r3-broken.md")
PY
```

## Boundary

Reproducing an anchor here asserts only that the bytes occur in the pinned
target; it adopts nothing and endorses nothing. The fixture exists so that the
claim "citation chaining is verdict-bearing" has fixed falsifiable inputs:
before the move, `verify` passes a hop whose anchor does not exist; after it,
`verify-chain` reports `anchor-missing`, drifts, and counts the resolved hops
exactly.