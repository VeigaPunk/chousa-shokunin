# R53DraftMistakes — round 53 w1: draft `## Mistakes` rows for `corpus/lessons/round-53.md`

seat: `R53DraftMistakes` (leaf; no dispatch) · date 2026-10-26 · lane `chousa-shokunin`.
Read first: `corpus/evidence/round53/claims.md` (frozen at `a6ff732`); HEAD `6365f15`, candidate `32aab5e`, BASE_REV `5b55013`.
No tool installed or upgraded (pacman paused host-wide; `python3` and `git show` sufficed). No network, no fetch; every source is a lane file or the read-only campaign package.
Nothing written outside this report: `git` calls are `show`/`rev-parse` only, and no production file, index, jj state or sibling lane was touched.
Scratch `/fast/scratch/hyaku/chousa-r53/R53DraftMistakes/` (`TMPDIR` set there), receipts pasted below before removal; the two drafted scripts run from that scratch copy, whose sha256 is given.

## Draft rows — for `corpus/lessons/round-53.md`, section `## Mistakes`

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. stale count: three committed sites state a `claims-erratum.md` range that stops short of the erratum's last bullet — `SCORECARD.md:2664` and `corpus/lessons/round-52.md:153` say E1–E4 against E1–E6 (`corpus/evidence/round52/claims-erratum.md:7,14,27,32,36,40`), and `SKILL.md:133` says `round51/claims-erratum.md` E1-E4 against E1–E5 (`corpus/evidence/round51/claims-erratum.md:5,31,35,39,43`) | all five files byte-identical at HEAD `6365f15` (working sha256 = HEAD sha256; `round-52.md` `fd827cf9…`, `SCORECARD.md` `c84cb2e5…`, `SKILL.md` `db1b0f42…`, `round-51.md` `b0dc9ef3…`, `claims-erratum.md` `4f423bb8…`) | round-52 closure `corpus/lessons/round-52-verifier-spotcheck.md:92` (§6.1) named the first two; the `SKILL.md:133` instance is new to this seat and nothing has carried it | three append-only `correction:` lines (verbatim below) + `corpus/evidence/round53/erratum-range-check.py` (drafted below). Shown able to fail: red `RANGES=3 STALE=3` rc 1 on the lane; green `RANGES=3 STALE=0` rc 0 on a mirror carrying only those corrections |
| 2. province framing: a refusal rests on "out of province" where `PROVINCE.md`'s own refusal list carries no such ground, while the staged entry's headline is a search-record field and so in province | `corpus/lessons/round-52.md:64` province cell `**out of province for its spine**` and reason `(PROVINCE: out of province, report, never absorb)`; repeated in prose at `:82`; inherited verbatim from `corpus/lessons/round-51.md:70`. `PROVINCE.md:10-15` refuses exactly four lanes (`kasegi`, `kengaku`, `kumitate`, `kagi`) plus live-target research — regulator currency is none of them; `PROVINCE.md:17` is the general rule, not a ground. Disputed at `round-52-verifier-spotcheck.md:77` (§4 last reject row: "the headline … is a search-record field and so in province. Guideline currency is one of its `Unknown` bullets, not its spine") and routed at `:93` (§6.2) | round-52 closure, non-author spot-check (`R52` closure); the r51 origin of the phrase was not noticed | three append-only `correction:` lines restating the durable ground (S133 duplicates the S111 URL; S130/S131 outside the frozen by-document set) + `corpus/evidence/round53/province-ground-check.py`. Shown able to fail: red `PROVINCE_ROWS=3 UNSUPPORTED=3` rc 1; green `UNSUPPORTED=0` rc 0 |
| 3. routed-defect latency: a defect routed in a closure stayed "still open" for two rounds while the fix sat in scratch, and on the real campaign package the base tool still prints the wrong label | named `.ufo/waves/round-51/w2/R51W2ReviewToolV2.md:42-45` F5 (`renumber S011→S003 held`; "`held` still covers a same-run twin though docstring L24-27 defines it as 'a Registry row already carries'"); routed `corpus/lessons/round-51-verifier-spotcheck.md:101`; patched in scratch `.ufo/waves/round-52/w1/R52ExecAdopterTwin.md:1-5`; not landed `corpus/lessons/round-52.md:26` and `round-52-verifier-spotcheck.md:95`; landed `32aab5e` (top comment `:28-34`, `twin` at `:488`, count at `:574`). In the base blob the docstring says `held` = "a URL a Registry row already carries" (`git show 5b55013:tools/assimilate-rows.py:26-28`) while `:435-436` labels an in-run twin `held`, and `:507` prints `HELD=len(cited)-len(rows)`, conflating the two | r51 W2 reviewer; r51 and r52 closures; this seat on the real package today | landed v4 + the twin-label check. Shown able to fail: base prints `S195	S118	held` with `CITED=6 APPEND=5 HELD=1` and the check exits 1; v4 prints `S195	S118	twin` with `CITED=6 APPEND=5 HELD=0 TWIN=1` and exits 0. The latency rule (lands, or re-discloses with a named blocker that quotes the naming seat, before the next closure is scored) is **not counted** — no check yet shows it able to fail |

## Receipts

```
$ sha256sum erratum-range-check.py province-ground-check.py
3ff1902dacfe9766e6ee551ce6600305e3080670cf6cd63565f59b9ba9172567  erratum-range-check.py
686256f949ae9dcb52787cb9786f5d3f3424eb3615a8f8225b22db2a5b0ee1ff  province-ground-check.py
$ python3 erratum-range-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
FAIL SCORECARD.md:2664 states E1-E4; erratum carries E1-E6; no anchored correction
FAIL SKILL.md:133 states E1-E4; erratum carries E1-E5; no anchored correction
FAIL corpus/lessons/round-52.md:153 states E1-E4; erratum carries E1-E6; no anchored correction
RANGES=3 STALE=3
rc=1
$ python3 province-ground-check.py --root /home/vgpnk/Projects/shokunin/chousa-shokunin
FAIL corpus/lessons/round-51.md:70 out-of-province ground with no PROVINCE.md refusal target (row carries none; list ['kagi', 'kasegi', 'kengaku', 'kumitate'])
FAIL corpus/lessons/round-52.md:64 out-of-province ground with no PROVINCE.md refusal target (row carries none; list ['kagi', 'kasegi', 'kengaku', 'kumitate'])
FAIL corpus/lessons/round-52.md:82 out-of-province ground with no PROVINCE.md refusal target (row carries ['offset']; list ['kagi', 'kasegi', 'kengaku', 'kumitate'])
PROVINCE_ROWS=3 UNSUPPORTED=3
rc=1
$ python3 erratum-range-check.py --root $S/mirror
RESOLVED SCORECARD.md:2664 states E1-E4; erratum E1-E6; correction reaches E6
RESOLVED SKILL.md:133 states E1-E4; erratum E1-E5; correction reaches E5
RESOLVED corpus/lessons/round-52.md:153 states E1-E4; erratum E1-E6; correction reaches E6
RANGES=3 STALE=0
rc=0
$ python3 province-ground-check.py --root $S/mirror
RESOLVED corpus/lessons/round-51.md:70 province ground restated by an anchored correction
RESOLVED corpus/lessons/round-52.md:64 province ground restated by an anchored correction
RESOLVED corpus/lessons/round-52.md:82 province ground restated by an anchored correction
PROVINCE_ROWS=3 UNSUPPORTED=0
rc=0
```

`$S/mirror` = symlinks to every scanned lane file except `SCORECARD.md`/`SKILL.md` copies, plus §"Corrections" appended to `SCORECARD.md`; nothing else differs, so the green run isolates the correction lines. The real package's campaign run (row 3), `$S` = the scratch above, all three `--entry` arguments of the assignment:

```
# base tool at BASE_REV 5b550133d79bc09c82d8965cce2e48c2598b8c3e
sha256(base.py)=10af959b2b87dad565717b84e68733caab6cb7a940d68fb1c52fca793d4c86f4
rc=0
CITED=6 APPEND=5 HELD=1
$ cut -f1-3 $S/o-base/renumber.tsv | grep -E "^(S185|S195)"
S185	S118	append
S195	S118	held
$ awk -F"\t" 'NR>1 && $1=="S195" && $3!="twin"{print "S195_LABEL=" $3; bad=1} END{exit bad?1:0}' $S/o-base/renumber.tsv
S195_LABEL=held (need twin)
rc=1
# landed v4 at 32aab5edd70e43145cae72ec872278f3bc6efba7
sha256(new.py)=32628bbc33d1d293e789b7d8f44cd769996e56678c40fd5f3943b50b8d8ed636
rc=0
CITED=6 APPEND=5 HELD=0 TWIN=1
$ cut -f1-3 $S/o-new/renumber.tsv | grep -E "^(S185|S195)"
S185	S118	append
S195	S118	twin
$ awk -F"\t" 'NR>1 && $1=="S195" && $3!="twin"{print "S195_LABEL=" $3; bad=1} END{exit bad?1:0}' $S/o-new/renumber.tsv
rc=0
```

`sha256(base.py)` equals the blob digest `.ufo/waves/round-52/w1/R52ExecAdopterTwin.md:4` records, so the scratch patch of round 52 was written against exactly this base. `git diff --stat 32aab5e HEAD -- tools/assimilate-rows.py` is empty: HEAD's tool is v4.

## Corrections (verbatim, append-only — each resolves one `path:line` above)

```
correction: corpus/lessons/round-52.md:153 (claims-erratum.md E1–E4) — the round-52 erratum carries E1–E6 (`- **E5` in-round narrowing, `- **E6` unbounded span-builder reader); read the range as E1–E6.
correction: SCORECARD.md:2664 (claims-erratum.md E1–E4) — the same erratum carries E1–E6; read the range as E1–E6.
correction: SKILL.md:133 (round51/claims-erratum.md E1-E4) — the round-51 erratum carries E1–E5 (`## E5` controls and supplements changed after the freeze); read the range as E1–E5.
correction: corpus/lessons/round-52.md:64 (out of province for its spine) — the reason is S133 duplicates the S111 URL (one key: two rows for one page, and the frozen C2 binding breaks) and S130/S131 lie outside the round's frozen by-document set; the staged headline (a regulator field record on 是否检索灰色文献) is a search-record field and so in province, and guideline currency is one of the entry's Unknown bullets, not its spine.
correction: corpus/lessons/round-52.md:82 (out of province for its spine) — as :64: the reported reject stands on the duplicate URL and the frozen by-document set, not on the document's province.
correction: corpus/lessons/round-51.md:70 (out of province for its spine) — the round-52 closure restates the reason: S133 duplicates the S111 URL and the document lies outside the round's frozen set; the headline is a search-record field and so in province.
```

## Drafted code — intended lane path `corpus/evidence/round53/erratum-range-check.py` (outside both frozen counters)

```python
#!/usr/bin/env python3
"""An erratum range quoted in prose must reach the erratum's last bullet.
Append-only: an anchored `correction:` line whose own range reaches the last
bullet resolves a stale occurrence; the stale text is never rewritten.
usage: erratum-range-check.py [--root DIR]   exit 0 clean, 1 stale, 2 usage."""
import pathlib, re, sys

RANGE_RE = re.compile(r"(corpus/evidence/round\d+/claims-erratum\.md)`?\s+E(\d+)\s*[\u2013\u2014-]\s*E(\d+)")
CORR_RE = re.compile(r"^correction:\s+(\S+?):(\d+)\b(.*)$")
BULLET_RE = re.compile(r"^(?:## |- \*\*)E(\d+)", re.M)
SCAN = ["SCORECARD.md", "SKILL.md", "README.md", "LOG.md", "SHONEN.md", "corpus/lessons/*.md"]

def main() -> int:
    root = pathlib.Path(sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else ".")
    paths = [p for pat in SCAN for p in sorted(root.glob(pat))]
    texts = {p: p.read_text(encoding="utf-8") for p in paths}
    corr = {}
    for t in texts.values():
        for i, line in enumerate(t.splitlines(), 1):
            m = CORR_RE.match(line)
            if m:
                corr.setdefault((m.group(1), int(m.group(2))), []).append(m.group(3))
    bad = hits = 0
    for p, t in texts.items():
        rel = p.relative_to(root).as_posix()
        for i, line in enumerate(t.splitlines(), 1):
            for m in RANGE_RE.finditer(line):
                hits += 1
                err = root / m.group(1)
                ids = BULLET_RE.findall(err.read_text(encoding="utf-8")) if err.exists() else []
                if not ids:
                    print(f"FAIL {rel}:{i} erratum {m.group(1)} absent or carries no E<n> heading/bullet")
                    bad += 1
                    continue
                last, stated = max(int(x) for x in ids), int(m.group(3))
                if stated == last:
                    continue
                if [c for c in corr.get((rel, i), []) if re.search(rf"E\d+\s*[\u2013\u2014-]\s*E{last}\b", c)]:
                    print(f"RESOLVED {rel}:{i} states E1-E{stated}; erratum E1-E{last}; correction reaches E{last}")
                else:
                    print(f"FAIL {rel}:{i} states E1-E{stated}; erratum carries E1-E{last}; no anchored correction")
                    bad += 1
    print(f"RANGES={hits} STALE={bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
```

## Drafted code — intended lane path `corpus/evidence/round53/province-ground-check.py`

```python
#!/usr/bin/env python3
"""A staged-entry refusal that rests on "out of province" must name a ground
PROVINCE.md's own Refuses list carries (a lane the lane refuses to), not a
subject the round merely did not freeze. Append-only: an anchored `correction:`
at the same path:line resolves the occurrence. Scope: decision rows that name a
staged entry file and carry refuse/reject; prose elsewhere is out of scope.
usage: province-ground-check.py [--root DIR]   exit 0 clean, 1 stands, 2 usage."""
import pathlib, re, sys

STAGED_RE = re.compile(r"`[a-z0-9-]+-r\d+(?:-amendment-\d{4}-\d{2}-\d{2})?\.md`")
DECISION_RE = re.compile(r"\brefuse|\breject", re.I)
PHRASE_RE = re.compile(r"out[ -]of[ -]province|PROVINCE:")
ARROW_RE = re.compile(r"\u2192\s*([a-z][a-z0-9-]*)")
CORR_RE = re.compile(r"^correction:\s+(\S+?):(\d+)\b")
SCAN = ["SCORECARD.md", "SKILL.md", "README.md", "LOG.md", "SHONEN.md", "corpus/lessons/*.md"]

def main() -> int:
    root = pathlib.Path(sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else ".")
    prov = (root / "PROVINCE.md").read_text(encoding="utf-8").splitlines()
    i = next(k for k, l in enumerate(prov) if l.startswith("**Refuses:**"))
    para = [prov[i]]
    j = i + 1
    while j < len(prov) and prov[j].strip():
        para.append(prov[j]); j += 1
    owned = set(ARROW_RE.findall(" ".join(para)))
    if not owned:
        print("USAGE PROVINCE.md carries no `-> lane` target in its Refuses paragraph")
        return 2
    texts = {p: p.read_text(encoding="utf-8")
             for pat in SCAN for p in sorted(root.glob(pat))}
    corr = {(m.group(1), int(m.group(2)))
            for t in texts.values() for line in t.splitlines()
            if (m := CORR_RE.match(line))}
    bad = hits = 0
    for p, t in texts.items():
        rel = p.relative_to(root).as_posix()
        for i, line in enumerate(t.splitlines(), 1):
            if not (PHRASE_RE.search(line) and STAGED_RE.search(line) and DECISION_RE.search(line)):
                continue
            hits += 1
            targets = set(ARROW_RE.findall(line))
            if targets & owned:
                continue
            if (rel, i) in corr:
                print(f"RESOLVED {rel}:{i} province ground restated by an anchored correction")
                continue
            print(f"FAIL {rel}:{i} out-of-province ground with no PROVINCE.md refusal target "
                  f"(row carries {sorted(targets) or 'none'}; list {sorted(owned)})")
            bad += 1
    print(f"PROVINCE_ROWS={hits} UNSUPPORTED={bad}")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main())
```

## Not done, and limits of these rows

- Nothing landed: the corrections are proposed text, the two checks are drafted code under intended lane paths, and the L1 integrates both. No lane file, index, jj state or sibling lane touched.
- Row 1's check reads only the five top-level lane docs plus `corpus/lessons/*.md`; a stale range inside `corpus/evidence/**` prose is out of its scope. Row 2's check is deliberately narrow (decision rows naming a staged entry) — the prose repeat at `round-52.md:82` is caught only because it carries both a staged filename and `reject`; a bare prose province claim elsewhere is not.
- Row 2's durable ground (S133 = S111, one key) is quoted from the round-52 Gate row and the closure; this seat did not re-open S133/S111 or the OLE `.doc` — that was the closure's, and re-measuring it is outside this seat.
- Row 3's "two rounds" is a date and pointer count (r51 lesson `2026-10-25` → r52 W1 scratch → landed r53), not a measured latency; and the latency rule itself has no failing check, so it is reported with the fix it would need rather than counted.
- Checked and **not** filed as a mistake: the frozen C1 sentence matches v4's bytes at the three points this seat exercised (`twin` label, `HELD=`/`TWIN=` counts, real package REAL-leg values `HELD=0 TWIN=1`); the base-tool S195 `held` reading reproduces `corpus/evidence/round53/claims.md`'s before-line.

VERDICT: attacked the lane's stale erratum ranges (3 sites, incl. one never routed), its "out of province" refusal ground (3 rows, inherited r51→r52, unsupported by `PROVINCE.md`) and the two-round adopter twin-label latency on the real package — all three proven red by a command with its output, and green only under the proposed append-only corrections, which are drafted here and not landed.
