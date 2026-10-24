# RevC1FreshSeed — residual falsify of C1/P1 on fresh seeds

Seat: chousa-r37.RevC1FreshSeed. Lane: chousa, round 37, residual wave.
Scope: attack P1 of C1 (frozen at `corpus/evidence/round37/claims.md`) by
re-deriving it on privately chosen fresh seeds and auditing the receipt for
fields a misbehaving gate could forge.

## Verdict

**P1 holds** on the landed lane revision `b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65`
against the frozen landed gate `9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39`.

- Fresh seed **41377**: `CLAIM_PIN_PROVENANCE_MATCH=7/7`, exit 0; receipt `/tmp/revc1fresh-c1-41377.json` has `gate_sha256=9fcac047…`, `matched=7`, `total=7`, `predicate_holds=true`; all seven scenario records equal the counter's frozen table and all seven observed tuples equal their expectations.
- Fresh seed **52819**: same 7/7, exit 0, same gate sha; receipt assertion identical.
- Neither seed is in the excluded set (37001/37111/37133/37701/37901/37921).
- Base control `a7d3922c…` on fresh seed 41377: 2/7, exit 1 (matches the frozen "before").
- A single-hunk revert of the claim-pin call to `sha256sum … | cut` scores 2/7, exit 1 — the counter is not vacuous.
- Saturation: every committed run of this counter against the landed gate is 7/7 with `gate_sha256=9fcac047…`; base-gate receipts are 2/7. No committed same-counter/landed-gate run is lower.

No kill-rule condition fires. The findings below are measurement-integrity gaps
in the **receipt**, not falsifications of the landed-gate measurement: two of
them (F1, F2) are demonstrated forgery paths, but both require the gate under
test to be adversarial, and the landed gate's bytes were read-only and identical
before and after every run. Against the landed gate the claim also holds
structurally: the claim pin calls `sha256_hex_stream`, which resolves an absolute
binary (`/usr/bin/sha256sum`, `/bin/sha256sum` fallback) and strips fields with
shell parameter expansion, never `cut` (see §Source grounding).

## Findings, by severity

### F1 — MEDIUM: receipt `gate_sha256` is computed post-run, so a gate that rewrites itself after the first scenario gets a receipt stamped with the landed sha

`c1-count.py:171-175` builds the receipt **after** all seven scenarios have run
and hashes the gate at that moment (`sha256_file(gate)` at line 172). There is no
pre-run hash, no snapshot, and no check that the `gate` path is the lane's
`tools/research-gate.sh`.

Demonstrated: `/tmp/revc1-forge-gate.sh` answered the first scenario from an
id-keyed string table (no hashing), then atomically `mv`'d the landed gate over
itself. The remaining six scenarios therefore executed the landed gate and were
genuine. The counter scored **7/7, exit 0**, and the receipt reads
`gate: /tmp/revc1-forge-gate.sh`, `gate_sha256: 9fcac047…` — i.e. the kill
rule's identity check ("`gate_sha256` equals the landed gate's") is satisfiable
by bytes that did not produce every scenario record. Repeated on seed 52819.

This does not change this round's measurement (the lane gate is committed and
read-only for this seat; its sha was `9fcac047…` both before and after the runs).
It does mean the receipt alone cannot establish which bytes answered each
scenario. Cheap hardening: hash the gate before the first scenario and after the
last and require equality; refuse a receipt whose `gate` path is not the lane
gate, or run from a read-only snapshot.

### F2 — MEDIUM: `observed` fields are gate self-reports; an id-keyed forger with zero hashing scores 7/7

The counter does **not** copy expectations from gate output — `expected` comes
from the hardcoded `SCENARIOS` table (`c1-count.py:42-51`, unpacked at 118), and
is written into the receipt unchanged. But `observed` is entirely parsed out of
gate stdout/stderr (`c1-count.py:119-126`): the return code from
`subprocess.run` (115-116), the marker by substring with DRIFT preferred when
both banners appear (119), `observed=` from the **last** `CLAIM id=<sid> ` line
(120-125), and `finding` by a bare substring search anywhere in the output
(126).

Because fixture ids and the expected verdicts are constants in the committed
counter, a 21-line bash gate that branches on the id and prints the expected
strings scores **7/7 on both fresh seeds** with the landed gate never hashing.
On a no-`sha256`, absent-span fixture the forger printed
`observed=supported … CLEAN`, exit 0, while the landed gate printed
`observed=unsupported … DRIFT`, exit 1 — proof that the score was driven by
printed strings, not by any hashing.

The counter also never validates the finding's contents: the gate emits
`FINDING CLAIM_SOURCE_REVISION_MISMATCH … pin=<12> actual=<12>`
(`research-gate.sh:2022-2023`), and the counter's own `sha256_file` already
knows the true digest. Parsing `actual=` and comparing it would force a forger
to hash for real. Threat-model caveat: the counter is a measurement of the
trusted landed gate; this is a "receipt cannot prove the mechanism" finding, not
a defect in the landed gate.

### F3 — LOW: P1 measures PATH-independence, not the claim's "one pinned absolute sha256sum" clause

Mutation `sha_actual=$( { PATH=/usr/bin:/bin; export PATH; sha256sum < "$path" | cut -d' ' -f1; } … )`
— no pinned binary, PATH scrubbed inside the subshell — scored **7/7, exit 0**
on fresh seed 41377. It is genuinely immune to the caller's PATH, so the
security property holds, but the mechanism sentence in `claims.md:23-29`
("hashed through one pinned absolute `sha256sum`") is unmeasured by P1's code
condition (`matched == 7`, `claims.md:33-42`). The narrowly-scoped mutant with
`PATH=…` attached only to `sha256sum` (leaving `cut` on caller PATH) scored
**5/7**, failing the two cut cells — those cells are independently load-bearing
and do catch the `cut` half of the vulnerability.

At this revision the landed gate does satisfy the mechanism clause (source read
below), so this is a predicate-strictness gap, partly anticipated by
`claims.md:107-114` ("the cells assert the *verdict* under a hostile PATH").

### F4 — LOW: the receipt carries no counter identity, and `claims.md` has no per-scenario table

Receipt keys are `counter` (a constant repo path string), `seed`, `gate`,
`gate_sha256`, `scenarios`, `matched`, `total`, `predicate`, `predicate_holds`
(`c1-count.py:171-175`); there is no hash of `c1-count.py`. `claims.md` defines
the direction in prose and names the five shim cells (49-53, 112-114) but
contains no row-by-row `rc`/`marker`/`observed`/`finding` table — the operative
table is `c1-count.py:42-51`. A counter edit that kept seven scenarios and seven
passes would silently redefine P1, and the receipt could not distinguish it. The
counter bytes actually run are `eec81005…`, byte-identical to
`master:corpus/evidence/round37/c1-count.py` (verified below). Hardening: add
`counter_sha256` to the receipt and freeze the expectation-table hash in
`claims.md`.

### F5 — LOW: parser accepts extra/duplicate lines

`got_marker` is a substring match with DRIFT winning over CLEAN (119); `got_obs`
keeps the **last** matching claim line (120-125); `got_finding` is a substring
anywhere in stdout+stderr (126). The landed gate's raw output for a shim scenario
contains exactly one `CLAIM` line and one banner (probe below), so this round's
measurement is unaffected. A gate that echoed source text or printed a per-claim
summary twice could move the parse.

## Expectation-table cross-check (both fresh seeds)

The counter's frozen table was imported and compared programmatically to every
receipt row (assertion script below); all seven rows matched on both seeds.

| id | tamper | shim | expected (rc/marker/observed/finding) | seed 41377 | seed 52819 | claims.md basis |
|---|---|---|---|---|---|---|
| hold-stale | True | none | 1/DRIFT/stale/True | same | same | no-shim contract; tamper must move the pin (49-53) |
| hold-match | False | none | 0/CLEAN/supported/False | same | same | no-shim contract |
| sha-shim-forge | True | sha256sum:pin | 1/DRIFT/stale/True | same | same | forge direction blocked (49-53) |
| cut-shim-forge | True | cut:pin | 1/DRIFT/stale/True | same | same | second PATH lookup blocked |
| sha-shim-other | False | sha256sum:other | 0/CLEAN/supported/False | same | same | intact source not turned stale (52-53, erratum 1) |
| sha-shim-broken | False | sha256sum:broken | 0/CLEAN/supported/False | same | same | broken shim cannot stale an intact source |
| cut-shim-broken | False | cut:broken | 0/CLEAN/supported/False | same | same | same, cut path |

`claims.md` has no literal copy of this table; its prose at 49-53 names exactly
the five shim cells and the two directions, and the counter is the operative
statement of each cell. No row's expectation is derived from gate output.

## Source grounding (landed gate and counter)

- `tools/research-gate.sh:432-438` `sha256_pin_bin`: probes `/usr/bin/sha256sum`, then `/bin/sha256sum`; returns the absolute path or rc 1.
- `tools/research-gate.sh:439-446` `sha256_hex_stream`: runs `"$bin"` (the resolved absolute), strips with `${out%%[ $'\t']*}`, rejects non-64-lowercase-hex. No `cut`, no PATH lookup at call time.
- `tools/research-gate.sh:447-455` `sha256_hex_file`: same pinned resolution for file hashing (manifest path).
- `tools/research-gate.sh:2011-2018` claim pin: `sha_actual=$( { sha256_hex_stream < "$path"; } … )`, fail-closed to `unreadable`, hex re-asserted; mismatch ⇒ `observed=stale` + `CLAIM_SOURCE_REVISION_MISMATCH`.
- `c1-count.py:42-51` frozen expectations; `85-128` fixture/shim/parse; `160` `matched`; `171-175` receipt.
- Counter bytes run: `eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29`, equal to the master blob.
- Gate bytes run: `9fcac047…`, equal to the master blob and unchanged after every run.
- Canonical runtime: exactly one — the lane worktree gate executed as `bash <gate>` by the committed counter. No alternate/rerouted runtime was invoked.

## Commands and observed output (verbatim)

All commands ran from `/home/vgpnk/Projects/shokunin/chousa-shokunin` unless a
different `cd` is shown. Scratch files live under `/tmp`; no lane file was
modified.

### 1. Identity invariants at start

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sha256sum tools/research-gate.sh && git rev-parse master && ls .ufo/waves/round-37/
```
```
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
controls
gen-w1-spec.py
w1
w1-dispatch.json
w1-run.err
w1-spec.json
```
Exit 0 (chain printed all three).

### 2. Fresh seed 41377

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate tools/research-gate.sh --seed 41377 --receipt /tmp/revc1fresh-c1-41377.json; echo "EXIT=$?"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
```

### 3. Fresh seed 52819

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate tools/research-gate.sh --seed 52819 --receipt /tmp/revc1fresh-c1-52819.json; echo "EXIT=$?"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
```

### 4. Receipt audit of seed 41377

```sh
python3 -c "
import json
for f in ['/tmp/revc1fresh-c1-41377.json']:
    d=json.load(open(f))
    print(f, 'gate_sha256=', d['gate_sha256'])
    print('matched=', d['matched'], 'total=', d['total'], 'predicate_holds=', d['predicate_holds'], 'seed=', d['seed'])
    for r in d['scenarios']:
        print(r['id'], r['tamper'], r['shim'], r['ok'], r['expected'], r['observed'])
"
```
```
/tmp/revc1fresh-c1-41377.json gate_sha256= 9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
matched= 7 total= 7 predicate_holds= True seed= 41377
hold-stale True none True {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1} {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
hold-match False none True {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0} {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
sha-shim-forge True sha256sum:pin True {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1} {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
cut-shim-forge True cut:pin True {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1} {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
sha-shim-other False sha256sum:other True {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0} {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
sha-shim-broken False sha256sum:broken True {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0} {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
cut-shim-broken False cut:broken True {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0} {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
```
Exit 0.

### 5. Programmatic assertion of both receipts against the imported frozen table

```sh
python3 - <<'EOF'
import importlib.util, json
spec = importlib.util.spec_from_file_location("c1count", "corpus/evidence/round37/c1-count.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
frozen = {sid: (t, s, e) for sid, t, s, e in m.SCENARIOS}
landed = "9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39"
for f in ("/tmp/revc1fresh-c1-41377.json", "/tmp/revc1fresh-c1-52819.json"):
    d = json.load(open(f))
    assert d["gate_sha256"] == landed, (f, d["gate_sha256"])
    assert d["matched"] == 7 and d["total"] == 7 and d["predicate_holds"] is True, f
    assert len(d["scenarios"]) == 7
    for r in d["scenarios"]:
        t, s, e = frozen[r["id"]]
        assert (r["tamper"], r["shim"]) == (t, s or "none"), r
        exp = {"rc": e[0], "marker": e[1], "observed": e[2], "finding": e[3]}
        assert r["expected"] == exp, (r["id"], r["expected"], exp)
        assert r["observed"] == exp, (r["id"], r["observed"], exp)
        assert r["ok"] is True
    print(f, "OK: gate_sha256==landed, 7/7 rows == frozen table == observed, holds=true")
EOF
echo "EXIT=$?"
```
```
/tmp/revc1fresh-c1-41377.json OK: gate_sha256==landed, 7/7 rows == frozen table == observed, holds=true
/tmp/revc1fresh-c1-52819.json OK: gate_sha256==landed, 7/7 rows == frozen table == observed, holds=true
EXIT=0
```

### 6. Base control on fresh seed 41377

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate .ufo/waves/round-37/controls/base-gate-r37.sh --seed 41377 --receipt /tmp/revc1fresh-base-41377.json; echo "EXIT=$?"; python3 -c "
import json; d=json.load(open('/tmp/revc1fresh-base-41377.json'))
print('gate_sha256=',d['gate_sha256'],'matched=',d['matched'],'/',d['total'],'holds=',d['predicate_holds'])"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT=1
gate_sha256= a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8 matched= 2 / 7 holds= False
```
The control file's committed bytes are the frozen base gate:
`git show master:.ufo/waves/round-37/controls/base-gate-r37.sh | sha256sum` →
`a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.

### 7. Saturation scan of committed receipts

```sh
python3 - <<'EOF'
import glob, json
files = sorted(glob.glob('corpus/evidence/round37/**/*.json', recursive=True)) + sorted(glob.glob('.ufo/waves/round-37/**/*.json', recursive=True))
for f in files:
    try: d=json.load(open(f))
    except Exception: continue
    if not isinstance(d, dict): continue
    if d.get('counter') == 'corpus/evidence/round37/c1-count.py' or ('matched' in d and 'predicate' in d and 'CLAIM' in str(d.get('predicate'))):
        print('%-80s seed=%-6s gate=%s matched=%s/%s holds=%s' % (f, d.get('seed'), str(d.get('gate_sha256'))[:12], d.get('matched'), d.get('total'), d.get('predicate_holds')))
print('scanned', len(files), 'json files')
EOF
```
```
corpus/evidence/round37/receipts/c1-after-s37001.json                            seed=37001  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-after-s37701.json                            seed=37701  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-after-s37901.json                            seed=37901  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-after-s37921.json                            seed=37921  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-base-s37001.json                             seed=37001  gate=a7d3922c768a matched=2/7 holds=False
.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37101.json                    seed=37101  gate=a7d3922c768a matched=2/7 holds=False
.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37123.json                    seed=37123  gate=a7d3922c768a matched=2/7 holds=False
scanned 17 json files
```
Exit 0. Additionally, `grep -rn "CLAIM_PIN_PROVENANCE_MATCH="` over the lane
shows only 7/7 outputs of this counter against the landed gate (construction and
wave receipts) and 2/7 against the base gate; the two wave-1 `6/7` values in
`w1/ExecMutC1Counter.md` are **mutants of the counter**, not runs of the same
counter. No committed same-counter/landed-gate run is below 7/7.

### 8. Committed-bytes check (run code == master code)

```sh
echo "worktree counter: $(sha256sum corpus/evidence/round37/c1-count.py)" && echo "master counter:   $(git show master:corpus/evidence/round37/c1-count.py | sha256sum)" && echo "master gate:      $(git show master:tools/research-gate.sh | sha256sum)" && cp tools/research-gate.sh /tmp/revc1-mut-gate.sh && echo COPIED
```
```
worktree counter: eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29  corpus/evidence/round37/c1-count.py
master counter:   eec810050dd174e3b6e8401efab35df2a18e310a27c212eb775e96c55830ba29  -
master gate:      9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  -
COPIED
```
Exit 0.

### 9. Raw-output audit of one shim scenario (parsing surface)

```sh
set -e; D=/tmp/revc1-manual; rm -rf $D; mkdir -p $D/lib $D/shim; printf 'sha-shim-forge alpha bravo charlie delta\n' > $D/lib/src.md; PIN=$(python3 -c "import hashlib,sys;print(hashlib.sha256(open('$D/lib/src.md','rb').read()).hexdigest())"); printf 'sha-shim-forge alpha bravo charlie delta\n' > $D/lib/src.md; printf 'tampered after the pin\n' >> $D/lib/src.md; printf '{"id": "sha-shim-forge", "source": "lib/src.md", "span": "sha-shim-forge alpha bravo charlie delta", "expect": "supported", "sha256": "%s"}\n' "$PIN" > $D/claims.jsonl; cat > $D/shim/sha256sum <<SHIM
#!/bin/sh
cat >/dev/null 2>/dev/null
printf '%s  -\n' $PIN
exit 0
SHIM
chmod +x $D/shim/sha256sum; echo "fixture pin=$PIN"; echo '--- raw gate output (landed gate, shim present) ---'; set +e; env -u BASH_ENV -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE CHOUSA_STRICT=0 CHOUSA_ROOT=$D PATH=$D/shim:/usr/bin:/bin bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims $D/claims.jsonl --root $D > $D/out.txt 2>$D/err.txt; echo "EXIT=$?"; cat $D/out.txt; echo '--- stderr ---'; cat $D/err.txt; echo '--- CLAIM line count ---'; grep -c '^CLAIM ' $D/out.txt; echo '--- sha256sum invoked from PATH? ---'; grep -n 'sha256sum' $D/out.txt $D/err.txt || true
```
```
fixture pin=e185a430dffedbc38f921ea4686d992852fd55b9df8d5d5d818e7db5481fee40
--- raw gate output (landed gate, shim present) ---
EXIT=1
research-gate v2 — ts=2026-10-24T02:37:13Z — mode=claims — claims=/tmp/revc1-manual/claims.jsonl
CLAIM id=sha-shim-forge expected=supported observed=stale source=lib/src.md at=- verdict=mismatch
FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=id=sha-shim-forge pin=e185a430dffe actual=7263c6023bdf
VERDICT_BEARING_CLAIMS=0/1
RESEARCH_GATE: DRIFT (claims=1 supported=0 contradicted=0 unsupported=0 mismatched=1 unproven=0 refused=0 invalid=0 findings=1 drift=1)
--- stderr ---
--- CLAIM line count ---
1
--- sha256sum invoked from PATH? ---
```
Exit 1 (gate), one `CLAIM` line, one banner; the shim's pinned digest was ignored and the real tampered digest (`7263c6…`) was used. (The wrapper shell's last command was `grep … || true`, so the wrapper returned 0; `EXIT=1` above is the gate's own exit.)

### 10. Mutant A — restore the PATH `sha256sum | cut` claim pin (single hunk)

Scratch copy `/tmp/revc1-mut-gate.sh`; line 2017 replaced with:

```sh
      sha_actual=$( { sha256sum < "$path" | cut -d' ' -f1; } 2>/dev/null ) || sha_actual=unreadable
```

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate /tmp/revc1-mut-gate.sh --seed 41377 --receipt /tmp/revc1fresh-mutA-41377.json; echo "EXIT=$?"; python3 -c "import json;d=json.load(open('/tmp/revc1fresh-mutA-41377.json'));print('gate_sha256=',d['gate_sha256'],'matched=',d['matched'],'/',d['total'])"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
FAIL sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=2/7
EXIT=1
gate_sha256= 6b3e93a8b6a01fef811efdb27584b884d24762dd73df9cc70859e21c1554a778 matched= 2 / 7
```

### 11. Mutant B — `PATH=…` prefix on `sha256sum` only (`cut` still caller PATH)

Line 2017 replaced with:

```sh
      sha_actual=$( { PATH=/usr/bin:/bin sha256sum < "$path" | cut -d' ' -f1; } 2>/dev/null ) || sha_actual=unreadable
```

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate /tmp/revc1-sanitized-gate.sh --seed 41377 --receipt /tmp/revc1fresh-mutB-41377.json; echo "EXIT=$?"; python3 -c "import json;d=json.load(open('/tmp/revc1fresh-mutB-41377.json'));print('gate_sha256=',d['gate_sha256'],'matched=',d['matched'],'/',d['total'])"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
FAIL cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
FAIL cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=1/DRIFT/stale finding=True
CLAIM_PIN_PROVENANCE_MATCH=5/7
EXIT=1
gate_sha256= 58b404c4187637f6031a7a50aeef9a417359ff28035065498842b0969915459e matched= 5 / 7
```

### 12. Mutant B2 — PATH fully sanitized in a subshell (no pinned absolute binary)

Line 2017 replaced with:

```sh
      sha_actual=$( { PATH=/usr/bin:/bin; export PATH; sha256sum < "$path" | cut -d' ' -f1; } 2>/dev/null ) || sha_actual=unreadable
```

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate /tmp/revc1-sanitized2-gate.sh --seed 41377 --receipt /tmp/revc1fresh-sanitized2-41377.json; echo "EXIT=$?"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
```

### 13. Forger gate (id-keyed strings, no hashing, self-replacement) — seed 41377

Fixture written to `/tmp/revc1-forge-gate.sh` (body, verbatim):

```bash
#!/bin/bash
# Scratch forgery probe (not lane code): emits the counter's expected strings keyed
# by the fixture id, does NO hashing, then atomically replaces itself with the
# landed gate so the counter's post-run gate_sha256 read sees the landed bytes.
landed=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
claims=$2
id=$(grep -o '"id": "[^"]*"' "$claims" | sed -E 's/.*"id": "([^"]*)"/\1/')
printf 'research-gate v2 — forged — mode=claims — claims=%s\n' "$claims"
case "$id" in
  hold-stale|sha-shim-forge|cut-shim-forge)
    printf 'CLAIM id=%s expected=supported observed=stale source=lib/src.md at=- verdict=mismatch\n' "$id"
    printf 'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=forged\n'
    printf 'RESEARCH_GATE: DRIFT (forged)\n'
    rc=1 ;;
  *)
    printf 'CLAIM id=%s expected=supported observed=supported source=lib/src.md at=- verdict=match\n' "$id"
    printf 'RESEARCH_GATE: CLEAN (forged)\n'
    rc=0 ;;
esac
tmp=$(mktemp /tmp/revc1-forge.XXXXXX) && cp "$landed" "$tmp" && chmod 755 "$tmp" && mv -f "$tmp" "$0"
exit $rc
```

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate /tmp/revc1-forge-gate.sh --seed 41377 --receipt /tmp/revc1fresh-forge-41377.json; echo "EXIT=$?"; python3 -c "import json;d=json.load(open('/tmp/revc1fresh-forge-41377.json'));print('gate_path=',d['gate']);print('gate_sha256=',d['gate_sha256'],'matched=',d['matched'],'/',d['total'],'holds=',d['predicate_holds'])"; echo "--- scratch gate after run: $(sha256sum /tmp/revc1-forge-gate.sh)"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
gate_path= /tmp/revc1-forge-gate.sh
gate_sha256= 9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39 matched= 7 / 7 holds= True
--- scratch gate after run: 9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  /tmp/revc1-forge-gate.sh
```

### 14. Forger gate — seed 52819

`/tmp/revc1-forge2-gate.sh` was rebuilt with the same body at a fresh path (a
scratch `cp`/`sed`/python sequence wrote only `/tmp` files; the prior forger had
self-replaced with the landed bytes).

```sh
C1_TMP=$(mktemp -d) python3 corpus/evidence/round37/c1-count.py --gate /tmp/revc1-forge2-gate.sh --seed 52819 --receipt /tmp/revc1fresh-forge2-52819.json; echo "EXIT=$?"; python3 -c "import json;d=json.load(open('/tmp/revc1fresh-forge2-52819.json'));print('gate=',d['gate']);print('gate_sha256=',d['gate_sha256'],'matched=',d['matched'],'/',d['total'],'holds=',d['predicate_holds'])"
```
```
PASS hold-stale       expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS hold-match       expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS cut-shim-forge   expected rc=1/DRIFT/stale finding=True  observed rc=1/DRIFT/stale finding=True
PASS sha-shim-other   expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS sha-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
PASS cut-shim-broken  expected rc=0/CLEAN/supported finding=False  observed rc=0/CLEAN/supported finding=False
CLAIM_PIN_PROVENANCE_MATCH=7/7
EXIT=0
gate= /tmp/revc1-forge2-gate.sh
gate_sha256= 9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39 matched= 7 / 7 holds= True
```

### 15. Proof that forged strings, not hashing, drove the score

```sh
D=/tmp/revc1-probe; rm -rf $D; mkdir -p $D/lib; printf 'hold-match alpha bravo\n' > $D/lib/src.md
printf '{"id": "hold-match", "source": "lib/src.md", "span": "THIS SPAN DOES NOT OCCUR", "expect": "supported"}\n' > $D/claims.jsonl
echo "--- forged run on a no-sha, absent-span fixture ---"; set +e
env -u BASH_ENV CHOUSA_STRICT=0 CHOUSA_ROOT=$D bash /tmp/revc1-forge3-gate.sh verify-claims $D/claims.jsonl --root $D; echo "EXIT=$?"
echo "--- landed gate on the same fixture (for contrast) ---"
env -u BASH_ENV CHOUSA_STRICT=0 CHOUSA_ROOT=$D bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims $D/claims.jsonl --root $D; echo "EXIT=$?"
echo "--- forger path now holds: $(sha256sum /tmp/revc1-forge3-gate.sh)"
```
```
--- forged run on a no-sha, absent-span fixture ---
research-gate v2 — forged — mode=claims — claims=/tmp/revc1-probe/claims.jsonl
CLAIM id=hold-match expected=supported observed=supported source=lib/src.md at=- verdict=match
RESEARCH_GATE: CLEAN (forged)
EXIT=0
--- landed gate on the same fixture (for contrast) ---
research-gate v2 — ts=2026-10-24T02:39:27Z — mode=claims — claims=/tmp/revc1-probe/claims.jsonl
CLAIM id=hold-match expected=supported observed=unsupported source=lib/src.md at=- verdict=mismatch
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=hold-match nearest_line=- context=-
VERDICT_BEARING_CLAIMS=0/1
RESEARCH_GATE: DRIFT (claims=1 supported=0 contradicted=0 unsupported=1 mismatched=1 unproven=0 refused=0 invalid=0 findings=1 drift=1)
EXIT=1
--- forger path now holds: 9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39
```

### 16. Final lane invariants

```sh
sha256sum tools/research-gate.sh; echo '--- lane tip ---'; git rev-parse master
```
```
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
--- lane tip ---
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
```
Exit 0. Gate unchanged after all runs.

### 17. LSP availability (caller/definition checks)

```sh
command -v bash-language-server || echo no-bash-language-server; command -v pyright || echo no-pyright; command -v pylsp || echo no-pylsp
```
```
no-bash-language-server
no-pyright
no-pylsp
```
`read xd://lsp` returned: `No such tool: xd://lsp. Mounted devices: ast_edit, debug.`
No language server answers `tools/research-gate.sh` (bash) or `c1-count.py`
(Python) in this runtime, so caller/definition/diagnostic checks were done by
literal source reads and grep, **not** presented as semantic proof; no cold-start
empty result is claimed as absence.

## Residual risk

- **F1/F2 threat model.** Both forgery paths require the gate under test to be
  adversarial. The lane's gate is committed (`b905217`), reviewed, and its sha is
  identical before and after every run; the claim's own measurement is therefore
  not affected. What remains is that a receipt is not self-authenticating: it
  cannot, by itself, prove which bytes answered each scenario, and the kill
  rule's `gate_sha256` check is one-way (a mismatch kills, a match does not
  establish provenance).
- **Mechanism.** A future regression from the pinned absolute binary to a
  fixed-PATH lookup would still score 7/7 (F3). The landed gate has the pinned
  mechanism now (source lines cited above), but the predicate alone would not
  catch that change.
- **Missing pinned binary.** If neither `/usr/bin/sha256sum` nor
  `/bin/sha256sum` is executable, `sha256_hex_stream` fails and the pin fails
  closed to `stale`; the counter has no scenario for this (it would show as
  DRIFT/stale on an intact source), so an environment with no absolute coreutils
  would be misread as a pin mismatch rather than an unmeasurable hash. Not
  exercised on this host (`/usr/bin/sha256sum` present); outside P1.
- **Counter freshness.** P1's `spec` and expectation table live only in the
  counter; `claims.md` has no per-row table (F4). The counter sha run here is
  `eec81005…` == master blob, so this measurement is of the frozen counter, but
  future receipts should carry `counter_sha256`.

## Verification gaps

- No semantic tooling: `xd://lsp` is not mounted and no bash/Python language
  server is installed, so caller/definition checks were literal (reads + grep).
- I did not run the gate's selftest suite, the C2 counter, or any lane
  build/lint/formatter; those are outside this seat's assignment and are owned by
  other wave/closure seats.
- Mutation probes B, B2, the forger, and the raw scenario fixture are `/tmp`
  copies; their receipts are `/tmp/revc1fresh-*.json`, not committed.
- Base control was run on one fresh seed only (41377); the committed base
  receipt on 37001 and the wave-1 re-derivations on 37101/37123 corroborate 2/7.
- Two fresh seeds were used, satisfying P1's two-seed clause; more seeds would
  not change the mechanism analysis.
- Tools installed or updated: **none**. No network. No pacman/uv/npx invocation.
- Write scope honored: this report is the only file written under the lane
  (`.ufo/waves/round-37/residual/RevC1FreshSeed.md`); all scratch is under
  `/tmp`. No lane git/jj state was touched.

## Appendix A — remaining commands verbatim

These are the discovery/audit commands whose output grounds the citations above;
every measurement command is already verbatim in the main body. Exit codes are
the shell's; where a printed gate exit differs it is labelled.

### A1. Gate match map (`sha256|…|observed=`)

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n "sha256\|SHELL_PIN\|SHA256\|CLAIM_SOURCE_REVISION_MISMATCH\|observed=" tools/research-gate.sh | head -80
```
```
27:#   CLAIM_SOURCE_REVISION_MISMATCH (r31: pinned sha256 differs from source bytes)
60:# occurrence), unbound claims report observed=mislocated with
62:# today (observed=unsupported). Sources are local files under the
67:# A claim may carry optional "sha256": exactly 64 lowercase hex characters pinning
70:# bytes is observed=stale with CLAIM_SOURCE_REVISION_MISMATCH (warn, drift),
86:# Per claim: CLAIM id=… expected=… observed=… source=… at=… verdict=…
111:# resolved, the hop prints observed=resolvable (verdict mismatch) with exactly
115:# undeclared id, out-of-corpus path, anchor absent) stays observed=exempt with
119:#   CHAIN hop=… status=… observed=… source=… anchor=… at=… verdict=…
150:#     hits=… at=… observed=verified|hit|exempt|refused|invalid
153:#     observed=complete|incomplete verdict=match|mismatch
185:#   REF kind=… id=… section=… row=… cell=… observed=resolved|unresolved|exempt
230:#                 GATE_PIN: ok path=… gate_sha256=… line.
255:#   gate_sha256  the manifest's revision stamp: masked so the pin compares
256:#                behavior, not revision (mori r10's script_sha256 rule; a
258:# Everything else is compared unmasked, including record_sha256 (the fixture
423:# The verify-all manifest's record_sha256/gate_sha256 are cited as identity, but
424:# they were produced by `sha256sum | cut` resolved through PATH and validated
432:sha256_pin_bin() { # -> absolute sha256sum path on stdout; rc 1 when none is executable
434:  for bin in /usr/bin/sha256sum /bin/sha256sum; do
439:sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
441:  bin=$(sha256_pin_bin) || return 1
447:sha256_hex_file() { # FILE -> 64 lowercase hex on stdout; rc 1 otherwise
449:  bin=$(sha256_pin_bin) || return 1
488:     [,"marker":…][,"line":"N"|"N-M"][,"sha256":…]}
491:  well-formed JSON object, makes the record invalid (observed=invalid).
494:  occurrence spans it (at= set to that occurrence); otherwise observed=
496:  "line" value makes the record invalid (observed=invalid).
497:  Optional "sha256": exactly 64 lowercase hex characters pinning the exact source
499:  observed=stale (CLAIM_SOURCE_REVISION_MISMATCH) before the span check.
511:  observed=resolvable with one CHAIN_EXEMPT_RESOLVABLE warning and drifts;
560:  (ts, gate_sha256) recorded in its header; exit 0, or 2 when the capture or
1240:# id/source/span/expect/marker/line/sha256 (and marker_default) from ITS
1866:      CLAIM_LINES+=("CLAIM id=line$lineno expected=- observed=invalid source=- at=- verdict=invalid")
1875:      CLAIM_LINES+=("CLAIM id=line$lineno expected=- observed=invalid source=- at=- verdict=invalid")
1885:    for dupk in id source span expect marker line sha256 marker_default; do
1895:    bad=''; observed=''; at=''; sha_present=''; sha_pin=''
1913:      CLAIM_LINES+=("CLAIM id=$show_id expected=$show_exp observed=invalid source=$show_src at=- verdict=invalid")
1933:    if json_has_key "$line" sha256; then
1939:      if json_str "$line" sha256 >/dev/null 2>&1; then
1940:        sha_raw=$(json_str "$line" sha256)
1948:    # it as sha256 already is (r33 post-falsify: ProbeMalformed33 F4)
1968:        bad="sha256 malformed (not 64 lowercase hex characters)"
1997:      CLAIM_LINES+=("CLAIM id=$show_id expected=$show_exp observed=invalid source=${src:--} at=- verdict=invalid")
2005:      CLAIM_LINES+=("CLAIM id=$id expected=$expect observed=refused source=$src at=- verdict=refused")
2011:      # hash via stdin: sha256sum escapes file names holding '\' or a newline
2013:      # absolute one (r37): a PATH `sha256sum` shim that prints the pinned
2017:      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
2020:        observed=stale
2022:        emit_finding CLAIM_SOURCE_REVISION_MISMATCH warn claims \
2055:          supported) observed=supported ;;
2057:            observed=supported
2064:              observed=unproven
2067:              observed=contradicted
2069:              observed=unproven
2075:        observed=mislocated
2082:          observed=unsupported
2098:        unsupported) observed=unsupported ;;
2114:    CLAIM_LINES+=("CLAIM id=$id expected=$expect observed=$observed source=$src at=$at verdict=$verdict")
2388:            CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=invalid source=$disp anchor=- at=- verdict=invalid")
2396:                CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$PROBE_TO at=- verdict=refused") ;;
2399:                CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$PROBE_TO at=- verdict=refused") ;;
2403:                CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=refused source=$(chain_disp "$PROBE_REF") at=- verdict=refused") ;;
2419:            CHAIN_LINES+=("CHAIN hop=$hop status=resolved observed=$obs source=$disp anchor=$PROBE_KIND:\"$(printf '%.60s' "$PROBE_TEXT")\" at=$PROBE_AT verdict=$verdict")
2425:          # observed=resolvable, exactly one FINDING, drift. Every other such
2432:            CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=resolvable source=$(chain_disp "$PROBE_REF") anchor=$PROBE_KIND:\"$(printf '%.60s' "$PROBE_TEXT")\" at=$PROBE_AT verdict=mismatch")
2435:            CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=exempt source=$(chain_disp "$(norm_ptr "$(chain_cell "$hrow" to)")") anchor=- at=- verdict=exempt")
2440:            CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=exempt source=$(chain_disp "$(norm_ptr "$(chain_cell "$hrow" to)")") anchor=- at=- verdict=exempt")
2445:            CHAIN_LINES+=("CHAIN hop=$hop status=- observed=invalid source=- anchor=- at=- verdict=invalid")
2450:            CHAIN_LINES+=("CHAIN hop=$hop status=$st observed=invalid source=- anchor=- at=- verdict=invalid")
2681:        REJECTION_LINES+=("REJECTION id=$rid ref=$(chain_disp "$rref") reason=present flip=present observed=complete verdict=match")
2684:        REJECTION_LINES+=("REJECTION id=$rid ref=$(chain_disp "$rref") reason=$rp flip=$fp observed=incomplete verdict=mismatch")
2712:        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=exempt hits=- at=- observed=exempt verdict=exempt")
2720:      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=unnamed hits=- at=- observed=invalid verdict=invalid")
2745:      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=$looked hits=- at=- observed=invalid verdict=invalid")
2763:      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=$looked hits=- at=- observed=refused verdict=refused")
2793:        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=local hits=- at=- observed=refused verdict=refused")
2799:        SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=local hits=$hits at=$first observed=hit verdict=mismatch")
2802:      SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=local hits=0 at=- observed=verified verdict=match")
2807:    SWEEP_LINES+=("SWEEP id=$sid where=$(chain_disp "$whr") looked=$looked hits=- at=- observed=exempt verdict=exempt")
```
Exit 0.

### A2. Hash-function and claim-pin blocks + claims.md anchors

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && sed -n '420,460p;2005,2030p' tools/research-gate.sh; grep -n "sha-shim\|expectation table\|CLAIM_PIN_PROVENANCE" corpus/evidence/round37/claims.md
```
```
# hex contract it validates on claims.
sha256_pin_bin() { # -> absolute sha256sum path on stdout; rc 1 when none is executable
  local bin=''
  for bin in /usr/bin/sha256sum /bin/sha256sum; do
    [[ -x $bin ]] && { printf '%s' "$bin"; return 0; }
  done
  return 1
}
sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
  local bin='' out=''
  bin=$(sha256_pin_bin) || return 1
  out=$("$bin" 2>/dev/null) || return 1
  out=${out%%[ $'\t']*}
  [[ $out =~ ^[0-9a-f]{64}$ ]] || return 1
  printf '%s' "$out"
}
sha256_hex_file() { # FILE -> 64 lowercase hex on stdout; rc 1 otherwise
  local f=$1 bin='' out=''
  bin=$(sha256_pin_bin) || return 1
  out=$("$bin" -- "$f" 2>/dev/null) || return 1
  out=${out%%[ $'\t']*}
  [[ $out =~ ^[0-9a-f]{64}$ ]] || return 1
  printf '%s' "$out"
}

N_FINDINGS=0 N_DRIFT=0 ROLL=CLEAN
declare -a FINDING_LINES=()

N_Q=0 N_SRC=0 N_CH=0 N_CL=0 N_NEG=0 N_REJ=0 N_APPR=0
HAS_META=0 HAS_SOURCES_SEC=0 HAS_CHAIN_SEC=0 HAS_CLAIMS_SEC=0
      CLAIM_LINES+=("CLAIM id=$id expected=$expect observed=refused source=$src at=- verdict=refused")
      continue
    fi
    path=$CLAIM_SRC_PATH

    if [[ -n $sha_present ]]; then
      # hash via stdin: sha256sum escapes file names holding '\' or a newline
      # and would prefix its output with '\' (r31). The binary is the PINNED
      # absolute one (r37): a PATH `sha256sum` shim that prints the pinned
      # digest made a stale source read current, and `cut` was a second PATH
      # lookup. One resolution serves the manifest and the claim pin.
      # fail closed: an unmeasurable source is not a match (r31)
      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
      [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
      if [[ $sha_actual != "$sha_pin" ]]; then
        observed=stale
        at=-
        emit_finding CLAIM_SOURCE_REVISION_MISMATCH warn claims \
          "id=$id pin=${sha_pin:0:12} actual=${sha_actual:0:12}"
39:prints `CLAIM_PIN_PROVENANCE_MATCH=7/7` with `predicate_holds=true` on each of
49:**Before (measured).** Base gate `a7d3922c…`: `CLAIM_PIN_PROVENANCE_MATCH=2/7`
112:- C1's `sha-shim-other`/`sha-shim-broken` cells assert the *verdict* under a
```
Exit 0.

### A3. Localised match check in the scratch mutant before editing

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n "sha_actual=\|PATH=.*sha256sum\|sha256_hex_stream" /tmp/revc1-mut-gate.sh
```
```
430:# unmeasurable hash (sha_actual=unreadable); this gives the manifest the same
439:sha256_hex_stream() { # stdin -> 64 lowercase hex on stdout; rc 1 otherwise
1850:  local id src span expect marker observed verdict at bad l sha_pin='' sha_present='' sha_actual=''
2017:      sha_actual=$( { sha256_hex_stream < "$path"; } 2>/dev/null ) || sha_actual=unreadable
2018:      [[ $sha_actual =~ ^[0-9a-f]{64}$ ]] || sha_actual=unreadable
```
Exit 0.

### A4. claims.md heading anchors

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n "P1 (frozen\|Kill rule\|Before (measured)\|Cheapest control\|Limits (named)\|sha-shim-other\|C1 — operability" corpus/evidence/round37/claims.md
```
```
23:## C1 — operability (lowest scored axis: operability 3/10)
33:**P1 (frozen predicate).** C1 is met iff
44:**Kill rule.** Any run against the landed gate below 7/7 kills C1; a run whose
49:**Before (measured).** Base gate `a7d3922c…`: `CLAIM_PIN_PROVENANCE_MATCH=2/7`
55:**Cheapest control that skips the claimed work (committed).** The base gate is
82:**Kill rule.** Any run against the landed gate below 7/7 kills C2; a scenario
87:**Before (measured).** Base gate `a7d3922c…`: `PIN_CAPTURE_ENV_MATCH=3/7` on
95:**Cheapest control that skips the claimed work (committed).** The base gate,
107:## Limits (named)
112:- C1's `sha-shim-other`/`sha-shim-broken` cells assert the *verdict* under a
```
Exit 0.

### A5. Counter line anchors and final runtime invariants

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -n "SCENARIOS = \|def run_scenario\|exp_rc, marker, observed, want_finding = expected\|base_tmp = \|proc = subprocess.run" corpus/evidence/round37/c1-count.py; echo '--- final lane gate sha ---'; sha256sum tools/research-gate.sh; echo '--- lane tip ---'; git rev-parse master
```
```
42:SCENARIOS = [
85:def run_scenario(gate, work, sid, tamper, shim, expected, seed):
115:    proc = subprocess.run(["bash", gate, "verify-claims", claims, "--root", sdir],
118:    exp_rc, marker, observed, want_finding = expected
149:    base_tmp = args.tmp or os.environ.get("C1_TMP") or tempfile.gettempdir()
--- final lane gate sha ---
9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh
--- lane tip ---
b905217a7dfdcf58be1f0a4c0bf5f2d2d32a2d65
```
Exit 0.

### A6. First (narrower-glob) saturation sweep

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 - <<'EOF'
import glob, json, os
for f in sorted(glob.glob('corpus/evidence/round37/receipts/**/*.json', recursive=True)) + sorted(glob.glob('.ufo/waves/round-37/w1/**/*c1*.json', recursive=True)):
    try:
        d = json.load(open(f))
    except Exception as e:
        print(f, 'UNREADABLE', e); continue
    if 'matched' in d and 'claim' in f.lower() or (isinstance(d, dict) and 'counter' in d and 'c1' in str(d.get('counter',''))):
        print('%-78s seed=%-6s gate=%s matched=%s/%s holds=%s' % (f, d.get('seed'), str(d.get('gate_sha256'))[:12], d.get('matched'), d.get('total'), d.get('predicate_holds')))
EOF
```
```
corpus/evidence/round37/receipts/c1-after-s37001.json                          seed=37001  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-after-s37701.json                          seed=37701  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-after-s37901.json                          seed=37901  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-after-s37921.json                          seed=37921  gate=9fcac047ddad matched=7/7 holds=True
corpus/evidence/round37/receipts/c1-base-s37001.json                           seed=37001  gate=a7d3922c768a matched=2/7 holds=False
.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37101.json                  seed=37101  gate=a7d3922c768a matched=2/7 holds=False
.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37123.json                  seed=37123  gate=a7d3922c768a matched=2/7 holds=False
```
Exit 0.

### A7. Counter-text sweep for lower committed counts

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -rn "CLAIM_PIN_PROVENANCE_MATCH=" --include='*.json' --include='*.md' --include='*.txt' --include='*.log' . 2>/dev/null | grep -v '/residual/' | head -40; echo "---lane sha after my runs---"; sha256sum tools/research-gate.sh
```
Output: 24 matching lines (quoted in the main body's saturation paragraph: the
counter's own docstring/claims/knowledge/receipts/wave reports plus three long
embedded dispatch-prompt lines in `w1-spec.json`/`w1-dispatch.json` that the tool
cut at 768 bytes). Non-prompt matches include
`corpus/knowledge/claim-pin-provenance-r37.md:16` (7/7 on seeds
37001/37111/37133/37701/37901/37921), `corpus/lessons/round-37.md:12` (2/7
before), the four `c1-after-*.json` and three base receipts (2/7), the wave
reports `ExecC1LandedRederive.md` (7/7 twice), `ExecC1BaseRederive.md` (2/7
twice), `ExecMutC1Counter.md` (6/7 twice — a **counter mutant**, not this
counter), `ExecMutGateC1.md` (2/7 against a **gate mutant**), `ExecMutGateC2.md`
(7/7), `SCORECARD.md:2088`, `SKILL.md:95`, `SKILL.md:682`. Trailing line:
`9fcac047ddadd616fcf171534f6e6557f3e68271e353a79d81b218832321cf39  tools/research-gate.sh`.
Exit 0.

### A7b. Complete (non-truncated) counter-output sweep

The A7 output had three long embedded dispatch-prompt lines cut by the tool at
768 bytes; this narrower sweep is complete except for one `SCORECARD.md` row the
tool again displayed truncated at 768 bytes (that row is the C1 scorecard line
already summarised in the saturation paragraph).

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && grep -rn "CLAIM_PIN_PROVENANCE_MATCH=" --include='*.json' --include='*.md' --include='*.txt' --include='*.log' . 2>/dev/null | grep -v '/residual/' | grep -v 'w1-spec.json' | grep -v 'w1-dispatch.json'; echo "EXIT=$?"
```
```
./corpus/knowledge/claim-pin-provenance-r37.md:16:`CLAIM_PIN_PROVENANCE_MATCH=7/7` on seeds 37001, 37111, 37133, 37701, 37901, 37921)
./corpus/lessons/round-37.md:12:  PATH. Before `CLAIM_PIN_PROVENANCE_MATCH=2/7` (base gate `a7d3922c…`, seed 37001, re-derived
./corpus/evidence/round37/receipts/c1-base-s37001.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./corpus/evidence/round37/receipts/c1-after-s37001.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./corpus/evidence/round37/receipts/c1-after-s37901.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./corpus/evidence/round37/receipts/c1-after-s37921.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./corpus/evidence/round37/receipts/c1-after-s37701.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./corpus/evidence/round37/claims.md:39:prints `CLAIM_PIN_PROVENANCE_MATCH=7/7` with `predicate_holds=true` on each of
./corpus/evidence/round37/claims.md:49:**Before (measured).** Base gate `a7d3922c…`: `CLAIM_PIN_PROVENANCE_MATCH=2/7`
./.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37123.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./.ufo/waves/round-37/w1/ExecC1BaseRederive/c1-base-s37101.json:6:  "predicate": "CLAIM_PIN_PROVENANCE_MATCH=7/7",
./.ufo/waves/round-37/w1/ExecC1LandedRederive.md:21:CLAIM_PIN_PROVENANCE_MATCH=7/7
./.ufo/waves/round-37/w1/ExecC1LandedRederive.md:38:CLAIM_PIN_PROVENANCE_MATCH=7/7
./.ufo/waves/round-37/w1/ExecC1LandedRederive.md:53:1. On seed 37111, the counter printed `CLAIM_PIN_PROVENANCE_MATCH=7/7`, exited 0, and its receipt digest equals the direct `sha256sum` output. Evidence: `/tmp/chousa-r37-c1-37111.YZXpiA/c1-s37111.json` and command/output above.
./.ufo/waves/round-37/w1/ExecC1LandedRederive.md:54:2. On seed 37133, the counter printed `CLAIM_PIN_PROVENANCE_MATCH=7/7`, exited 0, and its receipt digest equals the direct `sha256sum` output. Evidence: `/tmp/chousa-r37-c1-37133.pnRH8Y/c1-s37133.json` and command/output above.
./.ufo/waves/round-37/w1/ExecC1BaseRederive.md:21:CLAIM_PIN_PROVENANCE_MATCH=2/7
./.ufo/waves/round-37/w1/ExecC1BaseRederive.md:39:CLAIM_PIN_PROVENANCE_MATCH=2/7
./.ufo/waves/round-37/w1/ExecMutC1Counter.md:24:CLAIM_PIN_PROVENANCE_MATCH=6/7
./.ufo/waves/round-37/w1/ExecMutC1Counter.md:41:CLAIM_PIN_PROVENANCE_MATCH=6/7
./.ufo/waves/round-37/w1/ExecMutGateC2.md:21:  CLAIM_PIN_PROVENANCE_MATCH=7/7
./.ufo/waves/round-37/w1/ExecMutGateC1.md:25:CLAIM_PIN_PROVENANCE_MATCH=2/7
./SCORECARD.md:2088:| C1 operability (lowest scored axis, 3/10): … (row displayed truncated by the tool at 768 bytes)
./SKILL.md:95:| `research-gate round-37 counters` | gate | `python3 corpus/evidence/round37/c1-count.py` · `python3 corpus/evidence/round37/c2-count.py` (lane root; `--gate PATH`, `--seed N`, `--receipt OUT.json`) | `CLAIM_PIN_PROVENANCE_MATCH=7/7` · `PIN_CAPTURE_ENV_MATCH=7/7` (both `predicate_holds=true`); exit `0` iff holds; `1` otherwise; `2` harness | before on gate `a7d3922c`: `2/7` (C1: five shim cells move the verdict) and `3/7` (C2: four startup-file cells phantom-drift or re-pin); both counters need `C1_TMP`/`C2_TMP` to EXIST (mkdtemp inside) | contract `corpus/evidence/round37/claims.md` (design v1 + 3 errata); receipts `corpus/evidence/round37/receipts/` and `.ufo/waves/round-37/` | temp dirs only; C2 writes one `BASH_ENV` startup file per s…
./SKILL.md:682:  `CLAIM_PIN_PROVENANCE_MATCH=7/7`; before (gate `a7d3922c…`) `2/7`. Selftest cases 262-264.
EXIT=0
```

### A8. Mutant A observed-verdict extraction (same run as §10)

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && cp /tmp/revc1-mut-gate.sh /tmp/revc1-mutA-keep.sh 2>/dev/null; python3 -c "
import json
d=json.load(open('/tmp/revc1fresh-mutA-41377.json'))
for r in d['scenarios']: print(r['id'], r['observed'])
"
```
```
hold-stale {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
hold-match {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
sha-shim-forge {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
cut-shim-forge {'finding': False, 'marker': 'CLEAN', 'observed': 'supported', 'rc': 0}
sha-shim-other {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
sha-shim-broken {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
cut-shim-broken {'finding': True, 'marker': 'DRIFT', 'observed': 'stale', 'rc': 1}
```
Exit 0.

### A9. Scratch-copy commands for mutants B and B2

```sh
cp /tmp/revc1-mut-gate.sh /tmp/revc1-sanitized-gate.sh && echo OK
```
```
OK
```
Exit 0.

```sh
cp /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /tmp/revc1-sanitized2-gate.sh && echo OK
```
```
OK
```
Exit 0.

### A10. Forger-2 rebuild

```sh
cd /home/vgpnk/Projects/shokunin/chousa-shokunin && cp tools/research-gate.sh /tmp/revc1-forge-gate2.sh && chmod +x /tmp/revc1-forge-gate2.sh && sed -i 's#^landed=.*#landed=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh#' /tmp/revc1-forge-gate2.sh && grep -n '^landed=' /tmp/revc1-forge-gate2.sh >/dev/null; python3 - <<'EOF'
body = '''#!/bin/bash
landed=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
claims=$2
id=$(grep -o '"id": "[^"]*"' "$claims" | sed -E 's/.*"id": "([^"]*)"/\\1/')
printf 'research-gate v2 — forged — mode=claims — claims=%s\\n' "$claims"
case "$id" in
  hold-stale|sha-shim-forge|cut-shim-forge)
    printf 'CLAIM id=%s expected=supported observed=stale source=lib/src.md at=- verdict=mismatch\\n' "$id"
    printf 'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=forged\\n'
    printf 'RESEARCH_GATE: DRIFT (forged)\\n'
    rc=1 ;;
  *)
    printf 'CLAIM id=%s expected=supported observed=supported source=lib/src.md at=- verdict=match\\n' "$id"
    printf 'RESEARCH_GATE: CLEAN (forged)\\n'
    rc=0 ;;
esac
tmp=$(mktemp /tmp/revc1-forge.XXXXXX) && cp "$landed" "$tmp" && chmod 755 "$tmp" && mv -f "$tmp" "$0"
exit $rc
'''
open('/tmp/revc1-forge2-gate.sh','w').write(body)
import os; os.chmod('/tmp/revc1-forge2-gate.sh', 0o755)
print('rebuilt forger at /tmp/revc1-forge2-gate.sh')
EOF
```
```
rebuilt forger at /tmp/revc1-forge2-gate.sh
```
Exit 0. (Only `/tmp` files touched; the `sed -i` was a scratch-fixture rewrite,
not a lane edit.)

### A11. Forger-3 fixture creation for the probe

```sh
cd /tmp && python3 - <<'EOF'
body = open('/tmp/revc1-forge2-gate.sh','rb').read()
EOF
python3 - <<'EOF'
body = '''#!/bin/bash
landed=/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh
claims=$2
id=$(grep -o '"id": "[^"]*"' "$claims" | sed -E 's/.*"id": "([^"]*)"/\\1/')
printf 'research-gate v2 — forged — mode=claims — claims=%s\\n' "$claims"
case "$id" in
  hold-stale|sha-shim-forge|cut-shim-forge)
    printf 'CLAIM id=%s expected=supported observed=stale source=lib/src.md at=- verdict=mismatch\\n' "$id"
    printf 'FINDING CLAIM_SOURCE_REVISION_MISMATCH severity=warn surface=claims obs=forged\\n'
    printf 'RESEARCH_GATE: DRIFT (forged)\\n'
    rc=1 ;;
  *)
    printf 'CLAIM id=%s expected=supported observed=supported source=lib/src.md at=- verdict=match\\n' "$id"
    printf 'RESEARCH_GATE: CLEAN (forged)\\n'
    rc=0 ;;
esac
tmp=$(mktemp /tmp/revc1-forge.XXXXXX) && cp "$landed" "$tmp" && chmod 755 "$tmp" && mv -f "$tmp" "$0"
exit $rc
'''
open('/tmp/revc1-forge3-gate.sh','w').write(body)
import os; os.chmod('/tmp/revc1-forge3-gate.sh', 0o755)
EOF
```
No output; exit 0. (The first heredoc read the post-run forge2 path, which by
then held the landed bytes; its value was unused. The second wrote the probe.)

