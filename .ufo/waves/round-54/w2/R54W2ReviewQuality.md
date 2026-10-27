# R54W2ReviewQuality — QUALITY 97–100: truth, checkability, conduct
Seat: reviewer, leaf. Claims frozen `5a1a2063` read with `claims-erratum.md` E1–E4; no predicate, target, counter or control
proposed for change. Scope: `corpus/QUALITY.md` 97–100 — every cited number, path:line and command opened or run; each check's
failing input shown; 98's named limit and 99's rule vs the round's conduct; numbering continuity. Scratch
`/fast/scratch/hyaku/chousa-r54/R54W2ReviewQuality` (removed at end; `TMPDIR` + `PYTHONDONTWRITEBYTECODE=1` exported for every
lane-counter run; `pgrep soffice.bin` empty after runs). No network, no fetch, no tool install (pacman paused; none needed). Lane writes: this file only.

## Numbering continuity — PASS
`grep -n '^9[0-9]\.\|^100\.' corpus/QUALITY.md` → `923:90 925:91 927:92 929:93 931:94 933:95 935:96 937:97 939:98 941:99 943:100`
— 90–100 each exactly once, no gap, no duplicate; 100 is the last line.

## 97 — all numbers reproduce except two transposed offsets and an unstated control-char convention
- `corpus/SOURCES.md:111` (raw line): S101 row anchors six quotes, label verbatim "UTF-16LE text of the raw .doc capture", stated
  `char 11170, 11205, 11993, 12161, 13247, 34374` ✓; `used-by` = `corpus/knowledge/citation-count-semantics-r37.md` ✓ (also 100's
  cite). `corpus/lessons/round-49.md:95-100`: exactly six `| S101 |` rows, lines 95–100 ✓ (grep `^\| S101`).
- `6dc68fd6b32ce9c8dfcebce8.raw` (sha256[:20] `6063a3aff7a4081e93a6`, 129,024 B), UTF-16LE decode: **64,512 chars ✓, 263 U+FFFD ✓**;
  C0 code points **18,451** (18,431 excl tab+LF; **18,242 excl tab+LF+CR**) — 18,242 needs CR (189) excluded too, unstated → F2.
  `.txt` sidecar exists (128,416 B); six phrase finds = `0,0,0,0,0,0` ✓ ("find → −1").
- `python3 tools/capture-text.py <raw>` → rc=0, **27,012 chars ✓, 0 U+FFFD ✓**; C0 = 469 × U+000A only — "0 control characters" is
  literal-false, true excluding tab/newline (folded into F2).
- `--locate` ×6 → `LOCATED count=1` ×6 ✓ at **11972, 12007, 12795, 12963, 14049, 25123**; form[N:] starts with the quote ✓ ×6.
  Criterion lists `…12,963 / 12,795…` at positions 3/4 — transposed → F1. True drifts: **+802 ×5, −9251** (criterion: +802, +802,
  +970, +634, +802, −9251). Stated-vs-located 0/6 ✓; "no constant repairs an old anchor" holds in the all-six sense (+802 does
  repair five of six).
- `corpus/evidence/round54/build-spans.py:107-113` ✓: `def raw_form` :107, `return b.decode("utf-16le", errors="replace")` :113 —
  the decode fallback for non-zip raws is live. Tool docstring rule ✓: wIdent 0xA5EC (:289-290), nFib ≥ 0xC1 (:295), Clx at
  fcClx/lcbClx (:307), cp1252/UTF-16LE pieces (:27-28), main story CP 0..ccpText (:29), field results only (:32).
- Repair path: `SCORECARD.md:2740-2748` corrections carry the TRUE mapping (`char11993->char12795`, `char12161->char12963`); dump
  `S101-text-form.txt` sha256[:12] `a8e3e7ad213b` = SCORECARD's `a8e3e7ad…` ✓; all six corrected offsets hold their quotes in the
  dump ✓; `python3 corpus/evidence/round53/pointer-anchor-check.py` → `ANCHORED=16/16 UNANCHORED=0 BAD=0` exit 0 ✓.

**F1 (97, medium — the criterion's own numbers fail its check for 2/6 phrases).** QUALITY.md:937 lists located offsets positionally
against the stated anchors; positions 3/4 are swapped vs what the tool prints and vs the round's landed corrections. Ran:
`--locate '本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。'` → `offset=12795` (criterion: 12,963);
`--locate '文献类型及载体类型标志'` → `offset=12963` (criterion: 12,795). Drifts +970/+634 are really +802/+802. Conclusion (0/6, no
uniform repair) unaffected; the two cited offsets are not reproducible.

**F2 (97, minor — unstated counting conventions).** "18,242 control characters" reproduces only when tab, LF **and CR** are excluded
(all-C0 count 18,451; the C1 predicate's own convention — tab/newline allowed — gives 18,431). "0 control characters" for the
defined form is literal-false (469 U+000A). Both numbers need their exclusion sets named to be checkable as written.

## 98 — behavior reproduces exactly on both arms; two citation defects
- `c1-count.py:244-256` ✓: `def leg_real` :244; digest check → `ENV_CHANGED … exit 2` :246-250; `c.soffice("txt:Text (encoded):UTF8",…)`
  :252 with private profile `(work/"soffice-profile").as_uri()` :106; oracle-file checks :253-256. `:259-278` ✓: oracle-line holds
  (≥8 non-space, list-label drop), ratio 0.90–1.10 :273-275, two `PINNED_QUOTES` located `count=1` :276-278.
- `:114` ✓: `def run` → `subprocess.run([sys.executable, str(self.hook), self.tool, *args])` :115; hook materialized from the `HOOK`
  constant :104-105. `:70-76` ✓: `BAD` tuple :70-71 (the ten audit events, incl. `subprocess.Popen`, `os.exec`, `os.spawn` — the
  events covering the `*` families), `AUDIT_FORBIDDEN <event>` + `os._exit(97)` :74-75, `sys.addaudithook(hook)` :76.
- Five pins ✓ (`REAL` :56-62, 5 keys; `74ced3e9…` a byte twin of `54fe0734…` :55); two pinned quotes ✓ (:63-66); per-leg guard ✓
  (`--per-leg < 2` → usage exit 2, main).
- Ran landed tool: `python3 corpus/evidence/round54/c1-count.py --seed 97 --per-leg 2` → `REAL=PASS 5 captures`, `REGRESS=PASS r52
  ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']`, `LEGS=6/6 C1=PASS` exit=0 — exact match; tool sha256 `2c0140bc…` = `measure-after.txt`'s
  named tool-rev ✓ (E2's after-measurement ran these bytes).
- Ran my own soffice-shelling forge (scratch, sha256 `bda3a793…`): `GEN=FAIL ggen0.doc rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'`,
  `REAL=FAIL … rc=97`, `LEGS=0/6 C1=FAIL` exit=1 — the Check's falsification reproduces (all five hooked legs abort; REGRESS also
  fails, r52 `LEGS=0/9`).
- `corpus/evidence/round52/c1-count.py:215` ✓: `subprocess.run([sys.executable, tool] + args, …)` — REGRESS invokes the tool outside
  the hook, as the named limit says. Named limit's supplement: `controls/c1-forge.txt` ✓ — rebuilt forge (sha `f73ac5c3…`) passes
  the frozen counter 6/6 (two runs) and scores `SUPPLEMENT_LEGS=0/3`; CONST/NAIVE/REFUSEALL/SHELL 0/3 there; `measure-after.txt` —
  landed tool `SUPPLEMENT_LEGS=3/3` ×4 ✓ (E1).

**F3 (98, minor — "the SHELL control's receipt says the same" is false as to the count).** `controls/c1-controls.txt` SHELL block:
`NONWORD=PASS 3 sheets`, `MALFORMED=FAIL gmal0.doc rc=2 err=b'REFUSED ole-not-word: no WordDocument name\n'`, `LEGS=1/6` — it keys
refusals on a byte check before rendering, so it does not fail every hooked leg and does not print 0/6. The receipt confirms only
the rc=97 `AUDIT_FORBIDDEN` mode on GEN/ENCRYPTED/REAL. The criterion's forge (0/6) and the SHELL control (1/6) are different
tools; the sentence conflates them.

**F4 (98, minor — the "(ran)" forge's digest sits in no corpus/evidence receipt).** sha `9c8def9b…` occurs in committed
`.ufo/waves/round-54/w1-results.json:76` and W1 `R54DraftQuality.md:49-54`, in no `corpus/evidence/round54/` receipt (committed
control digests: `e53423bd…` SHELL, `f73ac5c3…` rebuild forge). The class reproduces (my forge `bda3a793…`), so the check stands,
but the exact cited artifact is not re-runnable from lane receipts. Cross-note: sibling `R54W2ExecQualityChecks` F5 says the
digest appears *only* in `R54DraftQuality.md:49-54` — it also appears in the committed `w1-results.json:76`.

## 99 — every cited value verifies; rule matches the round's conduct as spec'd; report not yet filed
- r53 `.ufo/waves/round-53/w2.ready` exists; content names `…/round-53/w2-dispatch.json` ✓; `w2.ready.dispatched` and
  `w2-results.json` ABSENT (ls) ✓; `/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:14` carries "W2: 43 seats
  dispatched" ✓; `.scratch/goal-20261026-hyaku-run9.md:126` carries "w2.ready orphaned - L1 exited before dispatcher marked wave" ✓.
- r53 W1: `w1.ready.dispatched` ts `2026-10-26T21:03:41` + 49 ids ✓; `w1-results.json` seats=49, results=49, 0 error fields ✓ — the
  Check's positive example verifies.
- r54 W1 now: marker ts `2026-10-26T22:40:28` (49 ids) and `w1-results.json` (seats=49, results=49, 0 error fields), both
  git-tracked ✓ — a filed report MAY call W1 dispatched citing these two.
- Draft-time claim attested: W1 `R54DraftQuality.md:112-114` — `w1.ready` (22:31:41), `w1.ready.partial` (43 ids, 22:38:19), no
  marker/results, dispatch lists 49 seats. The partial file was never committed (`git log --all -- .ufo/waves/round-54/w1.ready.partial`
  → empty), so that historical state rests on the W1 report's observation, not repo history.
- The round-54 report (`.ufo/reports/round-54/chousa.md`) does not exist yet (fleet dir holds only other lanes'; no lane reports dir
  for r54). The requirement is already wired into the round's own W2 spec: `w2-spec.json` carries verbatim "this round's report must
  cite `.ufo/waves/round-54/w1.ready.dispatched` and w1-results.json", and both artifacts exist — rule and conduct-as-specified
  agree; the label itself is checkable only once the report is filed.

## 100 — red-before and discrimination reproduce exactly; positive arm vacuous at the tip (disclosed)
- `corpus/SOURCES.md:111` used-by = `corpus/knowledge/citation-count-semantics-r37.md` ✓; `controls/c2-controls.txt` TOOLED block ✓:
  `BOUND=3/3 (min 2) … HELD_CITED=- HELD_BAD=1 … REF_ID_UNBOUND=3`.
- Scratch probes (ran; `--root $S/c2probe2 --lane-only`; lane SOURCES.md copy + one entry carrying `source: S101 — <HIT url>`):
  A (used-by stale) → `HELD_CITED=- HELD_BAD=1` / `REF_ID_UNBOUND=2` / `C2=FAIL` exit 1; B (used-by cell += the entry) →
  `HELD_CITED=S101 HELD_BAD=0` / `REF_ID_UNBOUND=0`; C (line mis-numbered `source: S090 — <url>`) → `HELD_CITED=- HELD_BAD=1` /
  `REF_ID_UNBOUND=2`. All three match the criterion's demo exactly; the counter reads the row from `--root` (lane untouched) ✓.
- Lesson records the cell as unchanged (E3) ✓ (Gate table "S101's `used-by` is therefore unchanged"; Census "no existing row
  touched"); `measure-after.txt`'s C2 block prints `HELD_CITED=- HELD_BAD=0`.

**F5 (100, minor — the positive arm is unreachable at the tip).** With E3's cut no entry carries `source: S101 — <HIT url>`, so at
the tip the held loop sees no citing entry and prints `HELD_CITED=- HELD_BAD=0` — vacuous, not earned; `HELD_CITED=<id> HELD_BAD=0`
fires only on a scratch root (probe B). The criterion's named limit ("the counter reads the row from `--root`, so a scratch copy can
be probed") discloses exactly this; recorded so the vacuity is not read as a pass over the S101 update rule.

## Residual risks / notes
- REGRESS runs the round-52 counter outside the hook (`round52/c1-count.py:215`): a delegating tool can pass REGRESS while failing
  the five hooked legs (disclosed; both forges failed REGRESS anyway). The oracle is one LibreOffice version; environment change →
  `ENV_CHANGED` exit 2, not a skip (c1-count.py :304-305) — disclosed.
- `build-spans.py:107-113` still returns the UTF-16LE decode for non-zip raws; no round-54 span touches an OLE `.doc` (S101 leg cut,
  E3) — disclosed limit, live for future spans.
- Lane `__pycache__` dirs exist under `corpus/evidence/round54/` (mtimes 23:14–23:19) and `round52/` (22:43) — created before this
  seat's runs (all of which exported `PYTHONDONTWRITEBYTECODE=1`); gitignored, attributed to earlier counter runs. No tool installed
  or upgraded (pacman paused; nothing needed). Only file written by this seat: this report; scratch removed after pasting receipts.

VERDICT: attacked QUALITY 97–100 by opening every cited path:line and re-running every check on the integrated tip — numbering 90–100
continuous; 98's both arms (landed `LEGS=6/6` / forge `LEGS=0/6` rc=97) and 99's four cited values reproduce exactly, and 100's A/B/C
red-before matches to the digit; 97 survives except two transposed located offsets (true 11993→12795, 12161→12963; criterion and its
drifts +970/+634 swapped vs tool and SCORECARD corrections) and two unstated control-char conventions (18,242 needs CR excluded; form
"0" needs tab/newline excluded); 98's "SHELL receipt says the same" is false (receipt: 1/6) and its forge digest sits in no
corpus/evidence receipt; 100's positive arm is vacuous at the tip under E3 (disclosed).
