# R87ExecHarm — C1 K3 harm sweep, wider than the round's own

Seat: R87ExecHarm. Claim: C1 `C1-BATTERY-R87` (operability). Kill rule under test: **K3** —
"a genuine committed record that the pre-round-87 tool accepts is refused at landing".
Trees: landed `e6e920a4` (scratch `$S`), base `6495ef88`, repo
`/home/vgpnk/Projects/shokunin/chousa-shokunin`. Base tool and landed tool differ by exactly
one line: `success = curl_rc == "0" and http == "200"` → `success = curl_rc == "0" and
200 <= int(http) < 300` (`diff` exit 1, 4 added comment lines + 1 changed line; receipts:
`a-harm-recheck.txt`, `b-full-sweep.txt`, `b-moved-records.txt`, `b-all-grep.txt`,
`c-positive-control.txt`, `c-genuine-s208.txt`, `d-probes-301-418.txt`).

## (a) Round's own harm control, re-run

Command: `python3 -B $S/corpus/evidence/round87/harm-recheck.py --root $S --repo
/home/vgpnk/Projects/shokunin/chousa-shokunin --base-tool <base gate-records.py>` (base blob
extracted at `6495ef88:tools/gate-records.py`).

Observed: `HARM_RECHECK files=11 records=28 moved=0 base_rc=0 r87_rc=0`, exit 0. Matches the
committed receipt `corpus/evidence/round87/controls/receipts/c1-harm-unreach.txt`
(`files=10 records=27 moved=0` at freeze; landing adds `corpus/lessons/round-87.md`, one
admit record, both tools OK). **Confirmed `moved=0`.**

## (b) Wider sweep — every committed `GATE-RECORD` line in the lane tree

Commands: `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin grep -rn '^GATE-RECORD'
e6e920a4 -- .` → 459 lines (369 files incl. 1 binary match; 368 text files), plus the same
over `corpus/lessons plans` (27 lines, 8 files) and `plans/` alone (**0 lines** — no
`GATE-RECORD` anywhere under `plans/`). Each file was run through both tools
(`verify --root $S --repo <lane> FILE...`, chunks of 50 files) and per-record verdicts
compared exactly (`(OK|FAIL, code)` tuples).

Observed: `FILES=368 BASE_RECS=458 LANDED_RECS=458; BASE OK=170 FAIL=288; LANDED OK=164
FAIL=294; MOVED=6`, every move `OK → FAIL REFETCH` (no `FAIL → OK`, no `FAIL → FAIL` code
change). The six, each a `decision=reject capture=none curl_rc=0 http=203` record over a
committed 203 refetch row:

| file:line | id |
|---|---|
| `.ufo/waves/round-85/w1/R85ExecForge/forge/n02-unreach-203-s021.md:1` | S021 |
| `.ufo/waves/round-85/w1/R85MutationTool/receipts/witnesses/W-M31-203-unreach.md:1` | S021 |
| `.ufo/waves/round-86/w1/R86ExecForge/records/c03-reject-success-203.md:1` | S021 |
| `.ufo/waves/round-86/w1/R86ExecForge/records/c06-reject-203-S022.md:1` | S022 |
| `.ufo/waves/round-86/w1/R86ExecForge/records/c08-reject-203-S032.md:1` | S032 |
| `.ufo/waves/round-86/w1/R86ScribeLesson/receipts/12-record-forms-probed.txt:60` | S021 |

**Classification (the K3 question).** All six are wave-produced attack/exhibit bytes, not
genuine committed records: `n02` and `W-M31-203-unreach` are the round-85 forge/mutation
witnesses for exactly the defect round 87 repairs (R85ExecForge F4 documents `n02` as the
"unreach on a 203 attempt is now accepted" case); `c03`/`c06`/`c08` are R86ExecForge's own
F1 candidates ("A `decision=reject` 203 record is accepted", plans/round-87.md defect 3);
`12-record-forms-probed.txt:60` is the probe-E exhibit quoting `c03`'s bytes. The base
tool's `OK` on them is the bug being repaired, and the landed tool's `FAIL REFETCH` is the
repair. No *genuine* lesson record moves: the lesson estate (`corpus/lessons/` + `plans/` =
28 tool-detected records over 27 grep lines, incl. the one `GATE-RECORD` mentioned in prose
at `round-86.md:122`'s block) is **28 OK under both tools, moved=0** — the genuine unreach
record `corpus/lessons/round-81.md:28` (S208, `curl_rc=22 http=403`) verifies OK on both
(receipt `c-genuine-s208.txt`).

Full census of `decision=reject capture=none` shapes in the tree (37 lines): only the six
above have `curl_rc=0 http=203`; every other 2xx unreach shape (`0/200` ×5, `0/201`,
`0/299`, `0/302`, `28/200` ×4, `7/203`) was already `FAIL REFETCH` on both tools (absence of
a matching row, or `curl_rc≠0` + no row), and `22/403` ×11 stays OK on both. The repair
changes no verdict outside the six defect exhibits.

## (c) Positive control — the sweep can fail

Probe (scratch only): `GATE-RECORD S021 url=https://pubmed.ncbi.nlm.nih.gov/17638714/
fetched=2026-11-08T02:15:39Z tier=A decision=reject capture=none curl_rc=0 http=404
words=0 quote=none` — a deliberately broken unreach record (404 claimed, the committed row
says 200/203). Observed: `FAIL REFETCH`, exit 1, on **both** tools. The sweep is not
vacuous: a mismatched unreach record is refused by base and landed alike, and the S208
genuine record stays OK on both (receipts `c-positive-control.txt`, `c-genuine-s208.txt`).

## (d) 3xx/4xx cannot be called success

Committed `refetch.tsv` (185 rows) has **zero** rows with `curl_rc=0` and `http` outside
`{200, 203}` — the only 3xx row is S135 `curl_rc=92 http=301`; there is no 418 row at all.
Probes against committed rows (receipt `d-probes-301-418.txt`):

- `curl_rc=92 http=301` over the S135 row: **OK on both tools** — the repair does not treat
  3xx as success; a failed transfer with a 301 is still a successful *unreach* record
  (success requires `curl_rc == "0"`). No verdict movement.
- `curl_rc=0 http=418` (no such row): `FAIL REFETCH` on both — refused by absence, not by
  the 2xx rule, and never called success.
- `curl_rc=0 http=302` over the S021 203 row: `FAIL REFETCH` on both (no matching row).
- `curl_rc=0 http=200` over the S217 200 fetch: `FAIL REFETCH` on both (2xx = success).
- `curl_rc=0 http=203` over each of S021/S022/S032: base OK, landed `FAIL REFETCH` — the
  2xx boundary is uniform across ids, not S021-keyed.

So the repair is exactly "any 2xx is a successful response, never a failed transfer":
3xx/4xx with `curl_rc≠0` still ground an unreach record, and 3xx/4xx with `curl_rc=0` are
accepted only when a refetch row exists (none does), never by the 2xx rule.

## Verdict

K3 holds. The only genuine committed records that could be harmed (the 28 lesson records,
28/28 OK on both tools) do not move; the six moves are precisely the defect exhibits the
round exists to refuse, each over one of the three qualifying 203 rows (S021, S032, S022).
No committed record accepted by the base tool that is not a 203 defect exhibit changes
verdict, and the probe set shows the sweep would have caught a real refusal.

Report: .ufo/waves/round-87/w1/R87ExecHarm.md
VERDICT: R87ExecHarm C1 held — the unreach repair moves no genuine committed record; all six verdict changes are the 203 defect exhibits the round repairs, over S021/S032/S022.
