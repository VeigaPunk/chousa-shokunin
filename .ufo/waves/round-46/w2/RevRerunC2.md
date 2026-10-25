# RevRerunC2 — C2 re-run and independent entry-point enumeration (round 46, wave 2)

Item: re-run `python3 corpus/evidence/round46/c2-count.py --root <tree> --list` over a `git archive`
of `d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a`; re-enumerate the entry-point set with my own script
(no import); compare set-for-set; report every difference with its cause.

Verdict: **C2 is not falsified at d09fc8e.** The re-run reproduces the declared after line
exactly, exit 0. My independent union, clipped to the counter's two path prefixes, is
**set-equal** to the counter's 72, and `counter \ mine = 0`. Set-for-set the counter misses
**exactly 8 existing repo-relative `.py`/`.sh` paths** (plus 2 absolute mentions no reading of
the predicate admits), each a control artifact — so the "counting command" clause survives,
but the exclusion comes from a prefix whitelist, not from that clause.

## 1. Re-run, verbatim

```
$ git -C …/chousa-shokunin archive d09fc8e7e2972e30e5e0aaa6e404c97aa0b9f95a | tar -x -C /tmp/chousa-r46w2-RevRerunC2/tree
$ cd /tmp/chousa-r46w2-RevRerunC2/tree
$ python3 corpus/evidence/round46/c2-count.py --root /tmp/chousa-r46w2-RevRerunC2/tree --list
ENTRY_POINTS=72 (tools=8 counters=50 named=70)
GATES_ROWS=35
REGISTERED=72/72
UNREGISTERED=0
C2=PASS
exit=0
```

Same output with no `--root` (LANE default), trailing slash, relative root, and through a symlink
(six invocations, one sha256 `a5e35b53af18…`); empty root → `C2=FAIL no-entry-points` exit 2.
Counter sha256 `60ad448e99b15cb6…` (blob `4b30bbe3773954a6…`), `SKILL.md` `2ff29159fa61…`,
`claims.md` `60098dfffe…`, `controls/c2-controls.txt` `a44c50c3e6ee…`; matches
`measure-after.txt:12-18` and the claims target line-for-line.

## 2. Independent enumeration, set-for-set

Script (no import): A = `os.scandir(tools/)`; B = regex on `corpus/evidence/round*/` basenames;
C = tokenizer `[A-Za-z0-9_./+-]+\.(py|sh)` over `SCORECARD.md` + `corpus/evidence/round*/claims*.md`,
keeping tokens that resolve (`realpath`-contained) to an existing file in root; rows from an
independent line state machine.

```
MY_A=8  MY_B=50  MY_C=78  MY_UNION=80      MY_REJECTED_ESCAPING=2      MY_GATES_ROWS=35
counter set = 72;  mine \ counter = 8;  counter \ mine = 0
A | B | (C ∩ {tools/, corpus/})  ==  counter set   →  True (72)
```

**The 8 differences** (all exist at d09fc8e; all `## Gates`-unregistered):

| path | naming document | role |
|---|---|---|
| `.ufo/waves/round-35/controls/ctl-c1-hardcoded-grep.sh` | `round35/claims.md:55` | "cheapest control that skips the claimed work" |
| `.ufo/waves/round-36/controls/base-gate-r36.sh` | `SCORECARD.md:2038`; `round36/claims.md:13` | byte-exact base-gate copy |
| `.ufo/waves/round-36/controls/ctl-c2-stub-pass.py` | `round36/claims.md:115` | "a witness that answers pass for everything" |
| `.ufo/waves/round-37/controls/base-gate-r37.sh` | `SCORECARD.md:2080`; `round37/claims.md:15` | byte-exact base gate |
| `.ufo/waves/round-38/controls/base-gate-r38.sh` | `round38/claims.md:231` | "a second control" |
| `.ufo/waves/round-39/controls/base-gate-r39.sh` | `SCORECARD.md:2217` | base-gate copy |
| `.ufo/waves/round-39/controls/mut-gate-path-env.sh` | `round39/claims.md:76` | single-hunk mutant control |
| `.ufo/waves/round-41/controls/base-gate-r41.sh` | `SCORECARD.md:2286` | `(control: --gate …)` |

Two further predicate-shaped tokens resolve outside the tree and are correctly out, the predicate
saying *repo-relative*: `../../../…/shokunin/scripts/sources-census.sh` (`SCORECARD.md:1591`) and
`…/.ufo/waves/round-29/falsify/DiffToolB/guarded-run.py` (`SCORECARD.md:1649,1661`).

**Cause, per difference:** `NAMED = r"(?:tools|corpus)/[A-Za-z0-9_./-]+\.(?:py|sh)"`. A `.ufo/` path
or an absolute path can never match that alternation, so the C leg sees only `tools/…` and
`corpus/…` occurrences: the counter is *mention-based within two directories* and never evaluates
the "counting command" qualifier. Correct here (all 8 misses are controls), wrong where a control
is the only thing named or a real instrument lives outside those prefixes. `MutC2Forge` already
listed the same 8 + 2 as an "undeclared exclusion"; new here is the set-equality proof and roles.
Secondary effect: a `./`-prefixed occurrence does not credit (lookbehind excludes `.` and `/`) —
row 114 as `./corpus/evidence/round34/self-audit.py` → `UNREGISTERED_PATH …/self-audit.py`, exit 1.

## 3. Rows and mutations

`## Gates` = `SKILL.md:75..507`, 35 counted rows at lines 79..117. All 72 have ≥1 row; 10 paths match
2 rows; `tools/research-gate.sh` matches 8. New rows: 113 (`round24–27`), 114 (`round33–34`), 116
(`inference-ground`), 117 (`chousa round-46 counters`, also naming `build-spans.py`).

```
delete row 116                  → REGISTERED=71/72 UNREGISTERED=1 GATES_ROWS=34 exit 1
row 114 names …self-audit.pyc   → UNREGISTERED_PATH corpus/evidence/round34/self-audit.py exit 1
row appended at EOF after `## ` → not a row (GATES_ROWS=30); replayed control holds
one 21-pipe row naming only the 16 unregistered of the before tree → 71/71 UNREGISTERED=0 C2=PASS exit 0
```

The `.pyc` line is the repair of `MutC2Forge`'s e2/e deviation: delimiter-bounded `names()`
refuses the substring credit the frozen blob allowed.

## Findings

1. **Medium — the committed control file already records the full-marks bypass, while the claim
   and the docstring say that shape is refused.** `controls/c2-controls.txt:50-56` records
   `--skill <SKILL-7pipe.md>` → `GATES_ROWS=31 REGISTERED=71/71 UNREGISTERED=0 C2=PASS exit=0`:
   one added row with ≥8 pipes registered all 16 previously-unregistered paths. `claims.md:69-71`
   lists four controls ("prose, six-cell row, eight-pipe row without `exit`, row after the next
   `## ` heading") and says they "all stay unregistered"; the file has seven runs, and
   `SKILL-fenced.md`, `SKILL-suffix.md` and this passing run go unmentioned. `c2-count.py:25-28`
   asserts "Cheapest gate that would score full marks without the work (QUALITY 60): pasting the
   bare paths anywhere in SKILL.md, or into a one-cell row — both are refused". Reproduced on the
   pre-state tree (base 6e2630a6 + the three counters, 55/71): one 21-pipe row naming only those
   16 paths → `GATES_ROWS=31 REGISTERED=71/71 UNREGISTERED=0 C2=PASS exit=0`. `MutC2Forge` row
   (a) found the mechanism for a *forged* row on the frozen blob; new here: the round's own
   artifact contains the PASS, the minimal cost is 16 paths / 21 pipes inside the section, and the
   QUALITY-60 sentence is false as written. **Not a kill** — row truth is the claim's named limit
   (`claims.md:72-73`), so this is a disclosure defect, not a predicate failure.
2. **Low — the C leg's document whitelist is blind to `measure-after.txt`.** d09fc8e adds
   `corpus/evidence/round46/build-spans.py`; `measure-after.txt:44-46` runs it as a gate
   (`SPANS_ROWS=11 STALE=0`, exit 0); `SCORECARD.md` at d09fc8e names it 0 times and no
   `claims*.md` names it → `"corpus/evidence/round46/build-spans.py" in counter_set → False`. It
   is registered by luck (row 117); removing only that name keeps `C2=PASS`. `RevC2Before` owns
   the `72 → 73` delta; this is why the counter cannot see the instrument before that row lands.
3. **Low — the one external gate is structurally unregisterable.** `sources-census.sh` is run as a
   verdict-bearing command by this round (`measure-after.txt:56-59`, exit 0; `SCORECARD.md:1591`)
   but is absolute and outside the lane, so "repo-relative" silently excludes it. Parser tolerance
   (info): the counter requires `line.startswith("|")` where my parser lstripped; no indented pipe
   line sits inside `## Gates`, so both give 35 rows.

## Residual risk and gaps

- Control fixtures `SKILL-*.md` are uncommitted (lane convention; round 45 ships `*.txt` only), so
  the seven controls reproduce in *shape* (my replays match `SKILL-7pipe` and `SKILL-after`) but
  not byte-for-byte — and finding 1 cannot be reconstructed from the repo.
- I did not re-run tools' exit codes or verdict maps; row truth is the named limit and belongs to
  `RevGatesRows` / `RevC2Rows`. No LSP server covers this tree, so cross-file claims here are
  text-grep matched, each paired with a measured run.
- The lane moved during this seat; all numbers above are `git archive d09fc8e`. At `HEAD`
  (`e50b388`, same counter sha256): `ENTRY_POINTS=73 … REGISTERED=73/73 UNREGISTERED=0 C2=PASS`
  exit 0, so the wave-2 fixes preserve the claim. Other seats later left an uncommitted counter at
  `c2729d7f…` (8+/4−) adding `(?:\./)?` and a raw-line row test; the `./` result above does not
  hold there, and it prints 73/73 PASS.
- No installs, no network, no writes outside this report; scratch `/tmp/chousa-r46w2-RevRerunC2/` deleted.
