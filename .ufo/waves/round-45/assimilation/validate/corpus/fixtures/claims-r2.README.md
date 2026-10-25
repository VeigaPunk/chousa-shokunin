# claims-r2.jsonl — pre-registered claim-vs-source fixture (chousa round 2)

Round-2 coverage move (dispatch 2026-10-15): the round-1 gate validates record
STRUCTURE only; no claim is ever checked AGAINST its cited source. This file
pre-registers the local-only claims fixture for the new
`verify-claims <claims-file>` mode, so the claim-vs-source check has fixed,
provenanced inputs and fixed expected verdicts before the implementation lands.

Authoring state: lane HEAD `6344569`, gate sha256
`08843552378071929c8b6abcd50be6613365691cfae4bf0d74fb03d86eb5b46e`.
`verify-claims` did not exist in the gate at authoring time; the fixture was
written as data plus this contract, not an executed-result claim. The
implementation landed later in the same wave, and this fixture then passed
end-to-end — see "Execution record" below. The byte-check command in "Re-run"
is executable independently of the gate and was run at authoring time.

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

`source` paths are fleet-root-relative; the re-run passes `--root ..` from the
lane cwd (the round-1 convention). Every path in this fixture resolves under
the allowed local corpus boundary (`research/deep-research-2026-09-28/`); no
external fetch, no URL, no session path. The fixture deliberately contains no
out-of-boundary path — the out-of-corpus refusal case belongs to the gate's
own selftest.

## Schema (one JSON object per line, UTF-8)

| field | meaning |
|---|---|
| `id` | unique id; letter = source input (A/B/C), number = entry |
| `claim` | the assertion a record would carry, readable prose |
| `source` | cited source, fleet-root-relative path (see pins above) |
| `span` | quoted span. For `supported`/`contradicted`: verbatim bytes copied from the source. For `unsupported`: the byte-exact quoted form that does NOT occur in the source |
| `expect` | the gate's expected per-claim adjudication: `supported`, `contradicted`, or `unsupported` |
| `marker` | present only on `contradicted` entries: the literal structural marker that must occur inside the span |

## Pre-registered verdict semantics

- `supported` — `span` occurs as a byte-exact substring of `source`, and no
  marker clause applies.
- `contradicted` — `span` occurs byte-exact and contains the entry's literal
  `marker`; the claim asserts the opposite of what the span says. The verdict
  is STRUCTURAL: the gate confirms span + literal marker, it does not do
  semantics.
- `unsupported` — `span` does NOT occur in `source`; the citation cannot be
  byte-verified. Negative controls, not adjudications of the claim's topic.
- The gate is expected to emit one verdict line per claim plus an exact
  counting summary, and `RESEARCH_GATE: CLEAN|DRIFT` under the existing exit
  contract (0 CLEAN | 1 DRIFT | 2 setup). CLEAN iff every observed verdict
  equals its `expect`; any mismatch, unreadable source, or out-of-boundary
  path imports drift.

Exact expected counts for this fixture — `claims=17 supported=13
contradicted=2 unsupported=2 mismatched=0`, exit 0 on CLEAN. These counts are
the fixture's ground truth; a summary that disagrees means gate drift.

## Marker convention

The `contradicted` verdict is structural, never semantic: the fixture records
the exact negation literal inside the span as the entry's `marker` field. A
`contradicted` entry whose span lacks its marker, or any non-`contradicted`
entry carrying a `marker`, is a fixture violation the gate should catch as
drift (the selftest's contradicted-without-marker case exercises the gate-side
refusal).

The two contradicted entries:

| id | marker | claim vs span |
|---|---|---|
| A05 | `could not substantiate` | claim asserts jin'i-ryū is an established rank; span records failed substantiation (A:64) |
| C06 | `is not a standard rank sequence` | claim asserts a standard rank sequence and a "self-legislating school" reading; span negates both (C:53) |

A06 is the paired near-miss: it is the A:52 universal-ladder sentence with
`do not` dropped (`They establish …`), so the span no longer occurs at all.
That is exactly the byte-level failure `unsupported` is meant to catch — an
inverted-meaning "quote" that a reading-level check could pass but a
byte-level check cannot. B05 is the same pattern against B:69's LEGOMem cell
(`assigns … exclusively to worker agents` vs the actual `Procedural memories
allocated to orchestrator and worker agents`).

## Provenance — what each entry exercises

| id | expect | source:line | role in the method |
|---|---|---|---|
| A01 | supported | A:52 | archive's own central model sentence; longest sentence span |
| A02 | supported | A:80 | customary periods, reformatted prose claim vs verbatim span |
| A03 | supported | A:81 | nine-year disciple account; typographic `ō` byte fidelity |
| A04 | supported | A:88 | graduated-responsibility reading, punctuation-bearing span |
| A05 | contradicted | A:64 | failed-substantiation form (the form RJ-02/CL-03 turned on) |
| A06 | unsupported | A:52 near-miss | dropped `do not` inverts the ladder sentence; span absent |
| B01 | supported | B:47 | export's own "closest match" claim |
| B02 | supported | B:64 | Voyager table cell, mid-line span boundary |
| B03 | supported | B:79 | ACE AppWorld numerals; digit-level byte fidelity (non-adoption note below) |
| B04 | supported | B:69 | LEGOMem table cell, contrast pair with B05 |
| B05 | unsupported | B:69 near-miss | fabricated exclusive-worker paraphrase; span absent |
| C01 | supported | C:89 | full-width `級`/`段` bytes inside a span |
| C02 | supported | C:92 | JKA examination wording, long span |
| C03 | supported | C:97 | Kendo shōgō titles; double `ō` byte fidelity |
| C04 | supported | C:102 | Todo/Murata history sentence, long span |
| C05 | supported | C:130 | Shu–ha–ri with en-dashes and `守破離` bytes |
| C06 | contradicted | C:53 | rank-sequence negation, arrow and typographic quotes |

## Boundary — spans are byte controls, not adopted knowledge

Reproducing a span here asserts only that the bytes occur in the pinned
source; it adopts nothing. In particular B03's numerals (18,282 / 122) come
from the kengaku-province benchmark material the round-1 intake deliberately
did not adopt (RJ-03) — they appear only because digit-level byte fidelity is
precisely where claim-vs-source verification matters. No span in this fixture
is domain knowledge, and a CLEAN run verifies span identity, not the semantic
truth of the source's own assertions.

## Execution record — 2026-10-15

Executed from the lane cwd against the settled implementation revision, gate
sha256 `03a3324455852ea0025115cb0e3ba9c8cdea10da5edc051c4738854a27c14be0`
(identical before, mid, and after the run), 23:25:00Z:

```text
bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
... 17 x CLAIM ... verdict=match (gate-reported at=line values 52, 80, 81, 88,
    64, -, 47, 64, 79, 69, -, 89, 92, 97, 102, 130, 53 — all agree with the
    provenance table above)
VERDICT_BEARING_CLAIMS=17/17
RESEARCH_GATE: CLEAN (claims=17 supported=13 contradicted=2 unsupported=2
mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
exit 0
```

At the same revision: `--selftest` → `RESEARCH_GATE_SELFTEST: PASS (30 cases)`,
exit 0 (the 20 round-1 cases plus 10 claims cases: pass, tampered,
out-of-corpus, external, session, contradicted-without-marker, stray-marker,
counting, and the two setup paths); the round-1 `verify` regression on archive
A is unchanged (exit 1, exactly one `RESEARCH_GATE: DRIFT` summary,
findings=6 drift=5). An earlier full pass at impl revision `dbf8a5e1…`
(23:18:26Z, exit 0) is a secondary observation; runs taken while the
implementation was still being written are not counted as acceptance.

## Re-run

From the lane cwd. Gate command:

```bash
bash tools/research-gate.sh verify-claims corpus/fixtures/claims-r2.jsonl --root ..
# expected: 17 per-claim verdicts; summary claims=17 supported=13 contradicted=2
# unsupported=2 mismatched=0; RESEARCH_GATE: CLEAN; exit 0
```

Independent byte-check of this fixture without the gate (run now; expected
output `counts {'supported': 13, 'contradicted': 2, 'unsupported': 2} bad []`):

```bash
python3 - <<'PY'
import hashlib, json, pathlib, collections
lane = pathlib.Path.cwd(); fleet = lane.parent
arch = fleet / "research/deep-research-2026-09-28"
for name, want in {
 "A-shokunin-tradition.md": "9033857d4625555c7b778dfad6df80e3e1b24ed8bffa3fee2fd445b9c5540b85",
 "B-multiagent-knowledge.md": "6d8dbddd3e2d2f47dcb153c5a3347cc6321db4afc72cf07da40f0f7fe5022006",
 "C-rank-taxonomy.md": "e48fe70ff92055c217ac6ca6ce68e403aa5689fee8717f3bd0ccf5badc92321b",
}.items():
    assert hashlib.sha256((arch / name).read_bytes()).hexdigest() == want, name
counts, bad = collections.Counter(), []
for n, line in enumerate(open("corpus/fixtures/claims-r2.jsonl", encoding="utf-8"), 1):
    e = json.loads(line)
    src = (fleet / e["source"]).read_text(encoding="utf-8")
    found = e["span"] in src
    if e["expect"] == "contradicted":
        ok = found and e["marker"] in e["span"]
    elif e["expect"] == "supported":
        ok = found and "marker" not in e
    else:
        ok = not found and "marker" not in e
    if not ok: bad.append((n, e["id"]))
    counts[e["expect"]] += 1
print("counts", dict(counts), "bad", bad)
PY
```
