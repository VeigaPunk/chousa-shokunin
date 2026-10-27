# R54DraftMistakes — draft `## Mistakes` rows for round-54

seat: `R54DraftMistakes` (scribe, leaf; no subagent dispatch) · date: 2026-10-26
scope: draft rows only. No lane file was written; every fix check below ran in scratch
`/fast/scratch/hyaku/chousa-r54/R54DraftMistakes` (removed at exit) with `TMPDIR` set there. No tool
install, no network, no LibreOffice (`pgrep -u $USER -f 'UserInstallation=file:///fast/scratch/hyaku/chousa-r54'`
→ `NO_SOFFICE_MINE`). Lane `HEAD` while I worked: `9caf8fc6e9113c8135f930503102eef0dd909e2e` (`master`).

## Draft rows (drop-in, round-53 4-column format)

| class | evidence pointer | captured-by | fix |
|---|---|---|---|
| 1. wave handoff reported as dispatched and merely late: the report writes "W2: 43 seats dispatched" and defers the wave's outcomes, while the wave has no dispatched marker, no results file and zero seat reports, and all 43 registry members carry `agentId: null` | `.ufo/waves/round-53/w2.ready:1` (the ready artifact); at `d21eb285ea2f7efa17e38d2df4f92588ab23122d` `git cat-file -e <rev>:.ufo/waves/round-53/w2.ready` → `W2READY_AT_TIP`, `.ufo/waves/round-53/w2.ready.dispatched` → `fatal: path ... does not exist in 'd21eb285'`, `.ufo/waves/round-53/w2-results.json` → same `fatal`; `.ufo/waves/round-53/w2/swarm-registry.json` = `mem 43`, `agentId_none 43 of 43`, `kinds {'spawn': 43}`, `createdAt 2026-10-27T00:25:05.042Z`, `updatedAt 2026-10-27T00:25:23.609Z`; `.ufo/waves/round-53/w2-dispatch.json` `counts {'spawn': 43, 'resume': 0, 'total': 43}`; fleet report `/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:14` ("**W2 WAVE-DONE/results had not arrived by the user's wrap directive; its seat outcomes and dead-seat count are unverified.**") and `:64` ("no dead-seat claim is made"); run file `/home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run9.md:126` "w2.ready orphaned - L1 exited before dispatcher marked wave" | round-53 verifier spot-check `corpus/lessons/round-53-verifier-spotcheck.md:13` read the absent `w2.ready.dispatched` + absent `w2/` seat reports as "consistent with the report's disclosed limitation", and `:79` (§6.2) routed the wave as "dispatched but WAVE-DONE/results never arrived"; the run file `:126` names the mechanism; re-verified this round by `R54DraftMistakes` (receipt R1) | run QUALITY 75's own check before filing — `python3 corpus/evidence/round50/wave-complete-check.py <wave-spec.json> <report-dir> --rev <tip> --lane .` — and write "dispatched" only where `<wave>.ready.dispatched` exists and every spec item has a report. Shown able to fail (receipt R1): round-53 w2 → 43 `MISSING` lines, `OK 0/43 reports present in .ufo/waves/round-53/w2@d21eb285`, `exit=1`; controls round-52 w2 → `OK 38/38`, round-53 w1 → `OK 49/49`, `exit=0` |
| 2. anchor in an undefined text form: nine quote offsets (S100 ×3 `corpus/lessons/round-49.md:92-94`, S101 ×6 `:95-100`) index a whole-file UTF-16LE decode that no lane command ever printed — it carries 263 U+FFFD, 243 `0x0b` separators and a binary preamble — so the offsets land elsewhere in the defined form (S101: `11170→11972`, `11205→12007`, `11993→12795`, `12161→12963`, `13247→14049`, `34374→25123`; S100: `1296→16`, `1431→151`, `2843→492`) | `corpus/SOURCES.md:110` (S100) and `:111` (S101): anchor cells read `(UTF-16LE text of the raw .doc capture); located quotes char 1296, char 1431, char 2843` and `... char 11170, char 11205, char 11993, char 12161, char 13247, char 34374`; `corpus/README.md:1138` "An OLE `.doc` keeps the UTF-16LE form (round 48)"; the base tool had no reader — `git show c49ffc6ce1c3de87c1dfa96856239ed7274bf07b:tools/capture-text.py <6dc68fd6…raw>` → stdout 0 bytes, stderr `REFUSED not a zip (an OOXML capture is a zip package)`, `exit=2`; `corpus/QUALITY.md:917` (87) requires a defined text form before a quote is located, and `corpus/QUALITY.md:800` (76)'s check still passes the defective file (`FORM_NAMED corpus/lessons/round-49.md`, `DECODE_FORM=PASS`, exit 0) because naming a decode is not defining one | `R54DraftMistakes` (this seat, first capture); round-49 W2 `ReopenS101` re-affirmed the offsets as correct (`ANCHOR [11170, 11205, 11993, 12161, 34374] ==QUOTEOFFS True`) by re-running the same ad-hoc decode, so the row was self-consistently wrong, not unchecked | re-anchor in the defined form and bind the check to locate-agreement (`anchor-form-check.py`, intended lane path `corpus/evidence/round54/anchor-form-check.py`, listing below): every lesson `char N` must equal `tools/capture-text.py <capture> --locate '<quote>'` and every SOURCES anchor `char N` set must equal those offsets. Shown able to fail (receipt R2): current files → 9 `MISMATCH` + 2 `set_equal=False`, `ANCHOR_FORM=FAIL mismatches=11`, `EXIT=1`; corrected copies in scratch (offsets above, form cell reading `text form: tools/capture-text.py, round 54 OLE reader`) → 9 `OK` + 2 `set_equal=True`, `ANCHOR_FORM=PASS`, `EXIT=0`. Not my write: the SOURCES.md anchor edit is the L1's |
| 3. runtime artifact left uncommitted at the round tip: W2's swarm registry (49,957 B, 43 members) existed only on disk at the round-53 tip and was inherited by round 54's freeze commit instead of being committed with its own round | `corpus/lessons/round-53-verifier-spotcheck.md:78` (§6.1: "`.ufo/waves/round-53/w2/swarm-registry.json` uncommitted at lane HEAD — commit or record why runtime registries stay untracked (w1's counterpart was committed)") and `:13` (working tree `?? .ufo/waves/round-53/w2/swarm-registry.json` (49,957 B, `ufo-swarm-registry-v1`, wave `chousa-r53-w2`, 43 members)); `git cat-file -e d21eb285:.ufo/waves/round-53/w2/swarm-registry.json` → `fatal: path ... exists on disk, but not in 'd21eb285…'`, `exit=128`; `git cat-file -e d21eb285:.ufo/waves/round-53/w1/swarm-registry.json` → `W1_REGISTRY_AT_TIP`; landed only in `5a1a206` ("inherit round-53 W2 registry") | round-53 verifier spot-check (non-author integrator), `corpus/lessons/round-53-verifier-spotcheck.md:13,78`; re-verified `R54DraftMistakes` (receipt R3) | a round may not close while a `.ufo/waves/<round>/**/swarm-registry.json` on disk is untracked at its tip: `git cat-file -e <tip>:<path>`, non-zero = the round is not committed. Shown able to fail (receipt R3): `d21eb28` → `exit=128`, `c49ffc6` (BASE_REV) → `exit=128`; after the inherit commit `5a1a206` → `exit=0`, `9caf8fc` (HEAD) → `exit=0` |

## Receipts (pasted verbatim; scratch copies removed with the scratch dir)

**R1 — QUALITY 75 check on the round-53 waves** (`cd /home/vgpnk/Projects/shokunin/chousa-shokunin`):

```
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-53/w2-spec.json .ufo/waves/round-53/w2 --rev d21eb285 --lane .
MISSING R53W2ExecC1Target
MISSING R53W2ExecSupplement
... (43 MISSING lines, first and last shown)
MISSING R53W2ExecAdopterBoundary
OK 0/43 reports present in .ufo/waves/round-53/w2@d21eb285
exit=1
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-52/w2-spec.json .ufo/waves/round-52/w2 --rev d21eb285 --lane .
OK 38/38 reports present in .ufo/waves/round-52/w2@d21eb285
$ python3 corpus/evidence/round50/wave-complete-check.py .ufo/waves/round-53/w1-spec.json .ufo/waves/round-53/w1 --rev d21eb285 --lane .
OK 49/49 reports present in .ufo/waves/round-53/w1@d21eb285
```

Presence/absence at the tip, and the registry's spawn bookkeeping:

```
$ git ls-tree --name-only d21eb285 .ufo/waves/round-53/ | grep -E 'w2'
w2-dispatch.json
w2-run.err
w2-spec.json
w2.ready
$ git cat-file -e d21eb285:.ufo/waves/round-53/w2.ready.dispatched
fatal: path '.ufo/waves/round-53/w2.ready.dispatched' does not exist in 'd21eb285'
$ git cat-file -e d21eb285:.ufo/waves/round-53/w2-results.json
fatal: path '.ufo/waves/round-53/w2-results.json' does not exist in 'd21eb285'
$ python3 -c "...registry..."
{'schema': 'ufo-swarm-registry-v1', 'wave': 'chousa-r53-w2', 'createdAt': '2026-10-27T00:25:05.042Z',
 'updatedAt': '2026-10-27T00:25:23.609Z', 'reportDir': '.ufo/waves/round-53/w2'}
members 43
agentId_none 43 of 43   kinds Counter({'spawn': 43})
$ ls -la .ufo/waves/round-53/w2/
-rw------- 1 vgpnk vgpnk 49957 Oct 26 21:25 swarm-registry.json     # no seat reports
$ cat .ufo/waves/round-53/w2.ready
{"lane":"chousa","round":53,"wave":"w2","dispatch":"/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-53/w2-dispatch.json","l1":"ChousaR53"}
```

The report sentence under test (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:14`):
"W2: 43 seats dispatched; dispatch role mix: 16 executor, … **W2 WAVE-DONE/results had not arrived by the
user's wrap directive; its seat outcomes and dead-seat count are unverified.**" — filed 21:33 local
(`ls -la`: `Oct 26 21:33`), eight minutes after `w2.ready` (21:25) and with `OK 0/43` seat reports on disk.

**R2 — anchor-form check (fails on the filed rows, passes on corrected copies)**:

```
$ python3 /fast/scratch/hyaku/chousa-r54/R54DraftMistakes/anchor-form-check.py corpus/lessons/round-49.md corpus/SOURCES.md
S100 rec=1296 defined=16 MISMATCH 中国知网他引频次的查询需要使用《中国引文数据
S100 rec=1431 defined=151 MISMATCH 对于合作发文的参考文献中，如果引文出现了任一
S100 rec=2843 defined=492 MISMATCH “文献来源”等方式进行组合查询，注：被引频次
S100 ANCHOR anchor=[1296, 1431, 2843] defined=[16, 151, 492] set_equal=False
S101 rec=11205 defined=12007 MISMATCH 每一篇文章或资料应根据其内容性质标识一个文献
S101 rec=11170 defined=11972 MISMATCH 为便于文献的统计和期刊评价
S101 rec=12161 defined=12963 MISMATCH 文献类型及载体类型标志
S101 rec=11993 defined=12795 MISMATCH 本规范推荐采用GB/T 7714中规定的顺序
S101 rec=34374 defined=25123 MISMATCH 参考文献格式，参照ISO 690
S101 rec=13247 defined=14049 MISMATCH 参照ISO 690及ISO 690-2，每一
S101 ANCHOR anchor=[11170, 11205, 11993, 12161, 13247, 34374] defined=[11972, 12007, 12795, 12963, 14049, 25123] set_equal=False
ANCHOR_FORM=FAIL mismatches=11
EXIT=1
$ python3 anchor-form-check.py round-49.corrected.md SOURCES.corrected.md
S100 rec=16 defined=16 OK ... (3 OK lines)
S100 ANCHOR anchor=[16, 151, 492] defined=[16, 151, 492] set_equal=True
S101 rec=12007 defined=12007 OK ... (6 OK lines)
S101 ANCHOR anchor=[11972, 12007, 12795, 12963, 14049, 25123] defined=[11972, 12007, 12795, 12963, 14049, 25123] set_equal=True
ANCHOR_FORM=PASS
EXIT=0
```

The undefined form, measured (`6dc68fd6b32ce9c8dfcebce8.raw`, sha256 `6063a3aff7a4…`, S101; the S100
capture is `b539a80218080da56a75b624.raw`, sha256 `46d1866ce9af…`, both as recorded in the lesson rows):

```
utf-16-le decode: fffd 263  len 64512  vtab 243  lf 6
head repr: '쿐\ue011놡\ue11a\x00\x00\x00\x00\x00\x00\x00\x00>\x03\ufffe\t\x06\x00…'
capture-text.py (8a7d0f1): defined_len 27012  fffd 0  vtab 0  head '中国学术期刊(光盘版)检索与评价数据规范\n（修订本）\n1 参考文献\n…'
base tool (c49ffc6) on the same bytes: exit=2, stdout 0 bytes, stderr 'REFUSED not a zip (an OOXML capture is a zip package)'
```

Existing check still green on the defective file — the loophole the fix must close:

```
$ python3 corpus/evidence/round50/decode-form-check.py corpus/lessons/round-49.md
FORM_NAMED corpus/lessons/round-49.md
DECODE_FORM=PASS
exit=0
```

**R3 — registry tracked at each rev** (`git cat-file -e <rev>:.ufo/waves/round-53/w2/swarm-registry.json`):

```
d21eb28 -> exit=128    # round-53 tip: on disk, not in the tree
c49ffc6 -> exit=128    # BASE_REV
5a1a206 -> exit=0      # 'round-54: freeze ... ; inherit round-53 W2 registry'
9caf8fc -> exit=0      # HEAD
```

## Notes for the L1 (integration, not rows)

- Row 1 wording: the three artifacts prove *no dispatched marker, no results, no seat report, no agent id*.
  They do not record a failed spawn call, so the draft says "43 registry members carry `agentId: null`" and
  leaves "never existed" to the L1's phrasing; `createdAt`→`updatedAt` is 18 s with no id attached.
- `round-53-verifier-spotcheck.md:13` says "dispatch evidence is committed": true of `w2-spec.json` /
  `w2-dispatch.json`, false of `w2.ready.dispatched`. If that line is to be corrected it is an append-only
  `correction:` in a round-54 site, not an edit of the round-53 file.
- Row 2's fix changes `corpus/SOURCES.md:110-111` anchors (rows opened 2026-10-23/25) and, if 87 is quoted,
  nothing else; the corrected copies I ran on are scratch-only and deliberately not in the lane.
- QUALITY 76's checker needs a `FORM_DEFINED` leg (locate-agreement, as in `anchor-form-check.py`); as it
  stands it certifies exactly the shape that failed here.

## Script listed for integration (intended lane path `corpus/evidence/round54/anchor-form-check.py`)

```python
#!/usr/bin/env python3
"""anchor-form-check — every row anchor's `char N` re-located through the defined text form."""
import re, subprocess, sys, pathlib
LANE = '/home/vgpnk/Projects/shokunin/chousa-shokunin'
TOOL = f'{LANE}/tools/capture-text.py'
QC = '/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache'
lesson, sources = sys.argv[1], sys.argv[2]
ids = sys.argv[3:] or ['S100', 'S101']
lines = pathlib.Path(lesson).read_text(encoding='utf-8').splitlines()
src = pathlib.Path(sources).read_text(encoding='utf-8').splitlines()
bad = 0
for sid in ids:
    offs = []
    for line in lines:
        if line.startswith(f'| {sid} |') and re.search(r'\| char \d+ \|', line):
            c = line.split(' | ')
            cap = f"{QC}/{re.search(r'`([^`]+)`', c[1]).group(1)}"
            rec = int(re.search(r'char (\d+)', c[2]).group(1))
            q = c[3].rstrip(' |').strip()
            r = subprocess.run(['python3', TOOL, cap, '--locate', q], capture_output=True, text=True)
            m = re.search(r'count=(\d+) offset=(-?\d+)', r.stdout or '')
            defined = int(m.group(2)) if m else None
            ok = m and m.group(1) == '1' and defined == rec
            bad += 0 if ok else 1
            if defined and defined >= 0:
                offs.append(defined)
            print(f'{sid} rec={rec} defined={defined} {"OK" if ok else "MISMATCH"} {q[:22]}')
    row = [l for l in src if l.startswith(f'| {sid} |')][0]
    anchor = [int(x) for x in re.findall(r'char (\d+)', row.split(' | ')[5])]
    same = anchor == sorted(offs)
    bad += 0 if same else 1
    print(f'{sid} ANCHOR anchor={anchor} defined={sorted(offs)} set_equal={same}')
print('ANCHOR_FORM=PASS' if not bad else f'ANCHOR_FORM=FAIL mismatches={bad}')
sys.exit(0 if not bad else 1)
```

VERDICT: attacked the three routed round-53/49 defects and built three draft `## Mistakes` rows — wave handoff (QUALITY 75 check: `OK 0/43` exit 1 against `OK 38/38`/`OK 49/49`), anchor form (9 of 9 filed offsets MISMATCH the defined form, `PASS` on corrected copies), uncommitted registry (`exit=128` at `d21eb285`/`c49ffc6`, `exit=0` from `5a1a206`); no lane file written.
