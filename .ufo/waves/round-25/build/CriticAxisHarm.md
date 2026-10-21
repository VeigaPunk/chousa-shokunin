# Round 25 Critic — Axis Harm

Scope: attack the pre-registration; judged axes are adjacency and depth. Also covering requested operability/freshness hazards. No gate/selftest was run; no installs.

Observed baseline only: `corpus/evidence/round25-measure-before.log:6-21` records 66 stale index items, 15 stale restatements, selftest PASS (136 cases), `GATE_DRIFT: none`, exports 3/3.

## Findings

### H1 — Operability: `METADATA_COMPLETE` can mean incomplete Criterion 6

Evidence: `corpus/QUALITY.md:17-23` requires a mined/used-by source row with URL/path and exact anchor, `verified-at` plus what was checked, and a specified recheck cadence/date. `corpus/evidence/round25-claims.md:29-40` checks presence, date prefix, and any `<N>d`; its summary says `METADATA_COMPLETE`.

[INFERENCE from the spec, not a run] The sample below is CLEAN by the specified predicates, yet fails Criterion 6: `S999` is not evidenced as a mined row, the date has no checked-what, and `7d` is not an allowed cadence.

Landing check (private clone): `tmp=$(mktemp -d); printf '%s\n' '# probe' 'source: S999 — https://example.invalid/x — §missing' 'verified-at: 2026-10-21' 'recheck: 7d' '' '## Body' >"$tmp/bad.md"; bash tools/research-gate.sh verify-metadata "$tmp/bad.md" --root "$tmp"; rc=$?; printf 'rc=%s\n' "$rc"; rm -rf "$tmp"`.

Smallest safe correction: call the frozen 28-entry result a **field-presence screen**, not Criterion-6 completion; validate Criterion 6 for newly admitted entries before claiming compliance.

### H2 — Depth: replacing stale summaries could erase substantive limits

Evidence: `SKILL.md:366-384` has archive-control evidence plus stale duplicated totals; `SKILL.md:386-432` has distinct behavioral limits for verify/claims/chain/sweeps/integrity/pin-drift. Cleanup is proposed in `round25-claims.md:64-70`.

Landing check: `python3 -c 'import pathlib,subprocess; b=subprocess.check_output(["git","show","b820e4e40ce52deedf53b191140cd7b08ddda929:SKILL.md"],text=True); n=pathlib.Path("SKILL.md").read_text(); e="No non-author corpus spot-check or promotion is implied by a passing selftest."; f=lambda s:s[s.index("**Limits.**"):s.index(e,s.index("**Limits.**"))+len(e)]; assert f(b)==f(n); print("SKILL detailed limits byte-identical")' && git diff --unified=3 b820e4e40ce52deedf53b191140cd7b08ddda929 -- SKILL.md`.

Smallest safe correction: replace only stale count/open-finding summaries with the ledger pointer and re-deriving command; preserve the detailed limits and archive-control account.

### H3 — Adjacency: new sources can import sibling-domain ground

Evidence: `CORPUS.md:98-122` scopes each source to a claim/topic and forbids duplicating the research method. Sibling boundaries route web publishing to kake (`kake-shokunin/PROVINCE.md:30-37`), model evaluation to kengaku (`kengaku-shokunin/PROVINCE.md:136-139`), dispatch to kumitate (`kumitate-shokunin/PROVINCE.md:24-28`), prompt/skill craft to kotoba (`kotoba-shokunin/PROVINCE.md:25-32`), and generic fixture craft to tameshi (`tameshi-shokunin/PROVINCE.md:40-47`). No new source rows were available to test; this is a conditional risk, not a claim of an actual boundary crossing.

Landing check: `git diff --unified=0 b820e4e40ce52deedf53b191140cd7b08ddda929 -- corpus/SOURCES.md corpus/knowledge corpus/README.md` — classify every added row/claim by its `scope`/`teaches`, not just its citation.

Smallest safe correction: keep new content to chousa's framing/source hierarchy/citation chain/claim-vs-source method; keep sibling product semantics as scoped examples or report-outs, not adopted chousa rules.

### H4 — Freshness: frozen counters miss new files and Frontier restatements

Evidence: `round25-measure.sh:27-33` tests a frozen base file list and presence of round labels; `:43-53` checks missing capability rounds. Its stale-restatement block reads only `SKILL.md` and `hardening-r10.md` (`:60-78`), so new Frontier text is unchecked. The new knowledge entry is in scope (`round25-claims.md:74-77`) but absent from the frozen base list. Therefore a zero count can coexist with an unindexed new note or a new stale restatement. `QUALITY.md:33-37` requires an owner/revision and re-deriving command for each restated number/finding.

Landing checks: `python3 -c 'from pathlib import Path; c=Path("corpus/README.md").read_text().split("## Frontier",1)[0]; fs=list(Path("corpus/knowledge").glob("*.md"))+list(Path("corpus/lessons").glob("*.md")); m=[r for p in fs if (r:=p.relative_to("corpus").as_posix()) and ("| `%s` |"%r) not in c]; print("CURRENT_UNINDEXED=",m); assert not m'` and `git diff --unified=0 b820e4e40ce52deedf53b191140cd7b08ddda929 -- corpus/README.md`.

Smallest safe correction: index every new knowledge/lesson file; review every added Frontier sentence containing mutable numbers/statuses for its owner, revision, and re-deriving command. Do not use the frozen count alone as proof.

### H5 — Operability: the recorded hold command does not prove cases 1–136 stayed identical

Evidence: prefix stability is required at `round25-claims.md:44-49`; `round25-measure.sh:81-83` retains only the final `--selftest` line, `--drift`, and export count. `round25-measure-before.log:17-21` has no case transcript. PASS totals cannot establish byte-identical prefix behavior.

Landing check (private clone):
```sh
tmp=$(mktemp -d); git show b820e4e40ce52deedf53b191140cd7b08ddda929:tools/research-gate.sh >"$tmp/base.sh"; bash "$tmp/base.sh" --selftest >"$tmp/base.out"; bash tools/research-gate.sh --selftest >"$tmp/new.out"
python3 - "$tmp/base.out" "$tmp/new.out" <<'PY'
import re,sys; read=lambda p:open(p).read().splitlines(); cases=lambda p:[x for x in read(p) if re.match(r"(?:ok|skip)-case\s+\d+\s",x)]; a,b=map(cases,sys.argv[1:]); assert len(a)==136 and b[:136]==a and all(x.startswith("ok-case") for x in b[136:]); assert read(sys.argv[2])[-1].startswith("RESEARCH_GATE_SELFTEST: PASS ("); print("SELFTEST_PREFIX_136_IDENTICAL; new cases pass")
PY
bash corpus/evidence/round25-measure.sh "$PWD"
```

Smallest safe correction: keep the prefix comparison as a landing assertion alongside existing `GATE_DRIFT` and 3/3 checks.

VERDICT: Depth/adjacency risks are preventable by narrow edits and scope review; the metadata-complete label and frozen-only measurements need the counterchecks above. Installs: none.