# R50ExecNegativeSweeps — replay every recheck/Unknown sweep in the three landed entries

Attacks: the `recheck:` line and every `#### Unknown` command of
`corpus/knowledge/cnki-citation-check-r40.md` (E1), `citation-matching-semantics-r41.md` (E2),
`istic-citation-verification-r39.md` (E3), at lane tip `c5b8dca` (landed content `74794db`).
Read-only captures under `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache`.
No scratch dir created (cwd used: `/dev/shm`, nothing written); no install, no fetch (L0 `8d77e6c1` open).

## 1. Replay table (command column = first 60 chars of the command as printed)

| # | entry | command first 60 chars | stated output | observed output | match |
|---|---|---|---|---|---|
| C1-U1 | E1 Unknown ¶1 | `cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansio` | `0 0` | `0 0` (rc 0) | yes |
| C1-U2 | E1 Unknown ¶2 ("the same command over four method words") | `print([t.count(w) for w in ['匹配','算法','字段','标识符']])` | `[0, 0, 0, 0]` | `NameError: name 't' is not defined` (rc 1) | **no — unreplayable** |
| C1-U3 | E1 Unknown ¶3 | `cd /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansio` | `4` `0` `0` `0` | `e3ca…75 4` / `2875…fb 0` / `275c…93 0` / `0012…8d 0` (rc 1) | yes |
| C1-U4 | E1 Unknown ¶4 | `print([t.count(w) for w in ['未找到','无结果','无匹配']])` | `[0, 0, 0]` | `NameError: name 't' is not defined` (rc 1) | **no — unreplayable** |
| C1-U5 | E1 Unknown ¶6 (staged corrections) | `print([t.count(w) for w in ['诚信档案','科研','人事']])` | `[0, 0, 0]` | `NameError: name 't' is not defined` (rc 1) | **no — unreplayable** |
| C2-R1 | E2 `recheck:` | `python3 -c "import sys;[print(len(t:=open(a,encoding='utf-8'` | `38174 0 4 5 0` / `30937 0 0 0 0` | same two lines (rc 0) | yes, only after `export QCACHE` |
| C2-R2 | E2 `recheck:` | `python3 -c "import sys;t=open(sys.argv[1],encoding='utf-8'.` | `30727 31262 535 [0, 0, 0, 0, 0, 0, 0, 0]` | `30727 31262 535 [0, 0, 0, 0, 0, 0, 0, 0]` (rc 0) | yes, same condition |
| C3-R1 | E3 `recheck:` on-disk half | `cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 ` | `SPANS_ROWS=11 STALE=0` | `SPANS_ROWS=55 STALE=0` (rc 0) | **no — number differs** |
| C3-U1 | E3 Unknown ¶1 (+ Inference ¶4) | `grep -cE '版本\|快照\|snapshot\|更新时间\|数据日期'` | `0` | `0` (rc 1) | yes |
| C3-U2 | E3 Unknown ¶2 | `grep -c 核对 / grep -c 匹配 / grep -c 查重 / grep -cE '全文\|原文'` | `0` `0` `0` `0` | `0` `0` `0` `0` | yes |
| C3-U3 | E3 Unknown ¶3 | `grep -c 复核 / grep -c 逐条` | `1` (three occurrences on it) / `0` | `1`; one line, `occ 3` / `0` | yes |
| C3-U4 | E3 Unknown ¶4 | `grep -cE 'CNKI\|知网'` | `0` | `0` | yes |

cwd: C1-U1/U3 and C3-R1 carry their own `cd` and reproduce from `/dev/shm`; C2-R1/R2 reproduce from
`/dev/shm` once `QCACHE` is exported; C1-U2/U4/U5 run nowhere (`NameError`); C3-U1..U4 run only in a
directory holding the capture, which the entry never names.

E1 `recheck:` text half (no re-download possible): `态共分为三种类型：` and `橙色` both
present once — `python3 -c "…print(t.count('态共分为三种类型：'), t.count('橙色'), …)"` → `1 1 30935 31063`,
i.e. the two offsets the entry states (char 30935, char 31063) hold. The E2 `recheck:` network half
("re-download the three copies and confirm §6.1 still opens 引文核对是指，以“中国知网”的文献资源为核对源内容")
is not executable offline; on-disk the phrase is `1` in `e3ca…75`, `0` in `2875…fb`, `0` in `0012…8d`,
and `6.1 引文核对` is `2`/`0`/`0` (heading + TOC).

## 2. Defects

**D1 — E3's `recheck:` states a number its own command cannot print (calibration, stated-output differs).**
`cd /home/vgpnk/Projects/shokunin/chousa-shokunin && python3 corpus/evidence/round50/build-spans.py --check`
→ `SPANS_ROWS=55 STALE=0`, rc 0, from the lane root and again from `/dev/shm` (cwd-independent: `LANE`
is derived from `__file__`, `build-spans.py:42`). The counter is global: `print(f"SPANS_ROWS={len(lines) - 1}
STALE={stale}")` (`build-spans.py:172`) over every row of `quotes.tsv`, which holds 55 rows
(`awk -F'\t' 'NR>1{print $1}' quotes.tsv | sort | uniq -c` → `18 S104 / 34 S105 / 3 S106`). `11` matches
neither the manifest (`18` S104 rows) nor the entry body (12 distinct `char N` values) nor the script.
`git log --oneline -- corpus/evidence/round50/build-spans.py` lists one commit (`6a068f2`), so the script
never printed 11 on this branch: the `recheck:` number was never observed. `STALE=0` does hold.
This is the lesson's own Mistakes row 1 class (number-drift) recurring in the same round.

**D2 — E1's three "the same command" legs are not commands (operability).**
Each is printed as a bare `print([t.count(w) …])` and binds `t` from the *previous* bullet. Replay fails
twice over: standalone (`NameError`, rc 1) and sequentially in one shell, because each is a separate
`python3 -c` process — `cmd1 && python3 -c "print([t.count(w) …])"` still prints `NameError` after `0 0`.
With `t` rebound the stated values do reproduce: `[0, 0, 0, 0]`, `[0, 0, 0]`, `[0, 0, 0]` — so the
substance holds and only the printed form is broken. The same defect means E1's `recheck:` "re-run the
four sweeps in `#### Unknown`" cannot be discharged literally.

**D3 — E1 `recheck:` says "four sweeps", `#### Unknown` carries five (calibration).**
Sweeps: ¶1 python3, ¶2 python3 fragment, ¶3 for-loop grep, ¶4 python3 fragment, ¶6 (corrections)
python3 fragment. The ¶6 sweep is a sweep; the count is stale by one.

**D4 — E2's `QCACHE` is defined in prose, not in the command (operability).**
The line reads "with `QCACHE=<path>`: `python3 -c …`". Pasted as one line the assignment does not
apply to `$QCACHE` in the same command's expansion: observed
`FileNotFoundError: [Errno 2] No such file or directory: '/e3ca8f4fdd15420b80096a75.txt'` (rc 1 — the
leading `/` is the empty variable). With `export QCACHE=…` in a prior step both commands run from
`/dev/shm` and reproduce `38174 0 4 5 0` / `30937 0 0 0 0` and `30727 31262 535 [0,0,0,0,0,0,0,0]`.
No `export` is printed anywhere in the entry.

**D5 — E2's `recheck:` asks for a check on three copies when only one can pass it (calibration).**
"re-download the three copies and confirm §6.1 still opens `引文核对是指，…`": the phrase occurs `1` time in
`e3ca…75` (S105), `0` in `2875…fb` (S106, which the entry itself reports as carrying 引文核对 0), `0` in
`0012…8d` (S104, not a source of this entry). The entry names two sources, so "three copies" is also
undefined in it. As printed the instruction fails for two of its three objects.

**D6 — E3's `#### Unknown` greps name no file (operability).**
All four are "over the capture"; the entry gives the URL, the char offsets and "capture `.txt` read as
UTF-8", never the filename. `grep -c '001287c436f0e6b1d166ae8d' corpus/knowledge/istic-citation-verification-r39.md`
→ `0`; the round-50 lesson does not name it either. The target is recoverable only by re-deriving
`sha256(url)[:24]` (`build-spans.py:51-52`) — i.e. by reading another tool. Once derived, every stated
number holds (table rows C3-U1..U4). Note the hazard: the same `更新时间` sweep run on the wrong capture
returns `1` (S105 carries `更新时间：2020 年 7 月` at char 48), so an unstated path is not harmless.

**D7 — exit status contradicts the printed output in two entries (operability, minor).**
C1-U3 and C3-U1..U4 end on a `grep -c` whose count is 0, so the commands print the stated numbers and
exit 1 (`rc=1` observed). Nothing in the entries states an exit code, so a replay harness that gates on
status marks a correct sweep as failed.

## 3. Secondary observation (adjacent to the replayed numbers, not a sweep)

E3's source line declares eleven offsets and the body uses twelve: `2.针对中国科学院用户：` at char 684 is
quoted in Observation ¶6 and in the manifest (`quotes.tsv` S104 row) but is absent from the source line's
offset list, while the `recheck:`/`verified-at` sentence says "the eleven quotes below". Registry row
`S104` (`corpus/SOURCES.md:114`, anchor cell) lists only six of them. Whether the row should carry all is
`R50ReopenRowS104`'s call; recorded here only because it is the number the `recheck:` line restates.

## 4. What found nothing

C1-U1, C1-U3 and (with `t` rebound) C1-U2/U4/U5 reproduce their stated values exactly; C2-R1/R2
reproduce exactly once `QCACHE` is exported; C3-U1..U4 reproduce exactly on the derived capture. The only
stated output that differs is C3-R1's `SPANS_ROWS=11`. No sweep depended on network, and no capture byte
was altered: `sha256sum` of the four captures gives `2197abe2…` (S105, as the entry states),
`c799044b…` (S106), `67f6f2df…` (S104), `8d201ed1…` (refused 教师 manual).

Attacked: every `recheck:`/`#### Unknown` sweep of E1–E3 replayed verbatim at lane tip `c5b8dca` —
**defect found**: E3's `recheck:` states `SPANS_ROWS=11` where its own command prints `SPANS_ROWS=55`
(global manifest count, never per-entry), E1's three "the same command" legs are unreplayable
(`NameError`) and its "four sweeps" is five, E2's `QCACHE` and E3's Unknown greps lack a runnable
definition/target; every stated count that is replayable reproduces exactly.
