# R54DraftQuality — QUALITY criteria 97-100 (append-only draft)

Seat: `R54DraftQuality` (scribe, leaf). Lane: `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Writes: this report only. Scratch `/fast/scratch/hyaku/chousa-r54/R54DraftQuality`, `TMPDIR` there,
removed at exit. No network, no pacman, no tool install; `/home/vgpnk/Projects/shokuknow` read-only.
Every check below was run by me; outputs pasted verbatim.

## 97 — a binary capture's text form is a defined, named reading, never a raw decode

Ran (the red-before, reproduced from capture bytes, not from the campaign's prose):

```
$ python3 - <<'PY'
raw=pathlib.Path('.../.qcache/6dc68fd6b32ce9c8dfcebce8.raw').read_bytes()
u=raw.decode('utf-16-le',errors='replace')
form=subprocess.run(['python3','tools/capture-text.py',RAW],capture_output=True,text=True).stdout
...
PY
raw-utf16le len= 64512 U+FFFD= 263 ctrl= 18242
defined-form  len= 27012 U+FFFD= 0 ctrl= 0
```

The six quotes the S101 row anchors (`corpus/SOURCES.md:111`, `corpus/lessons/round-49.md:95-100`),
located twice — once by decoding the container bytes, once by the lane tool:

```
$ for q in ...; do printf '%s\t' "$q"; python3 tools/capture-text.py $RAW --locate "$q"; done
为便于文献的统计和期刊评价	LOCATED count=1 offset=11972
每一篇文章或资料应根据其内容性质标识一个文献标志码	LOCATED count=1 offset=12007
文献类型及载体类型标志	LOCATED count=1 offset=12963
本规范推荐采用GB/T 7714中规定的顺序编码制格式著录,也可采用GB/T 7714中规定的作者-出版年制。	LOCATED count=1 offset=12795
参照ISO 690及ISO 690-2，每一参考文献条目的末尾均以“.”结束。	LOCATED count=1 offset=14049
参考文献格式，参照ISO 690	LOCATED count=1 offset=25123
```

Stated anchors 11170 / 11205 / 11993 / 12161 / 13247 / 34374 → drift +802, +802, +970, +634, +802,
−9251 (not a constant shift). The `.txt` sidecar (128416 chars) holds none of the six
(`find` → −1 each, ran). `build-spans.py:107-113` still returns the UTF-16LE decode for a non-zip raw.

## 98 — real inputs against a counting-time oracle, tool forbidden to delegate to it

Read (line numbers cited in the draft): `c1-count.py:70-76` (hook aborts `AUDIT_FORBIDDEN`, exit 97, on
`subprocess.Popen`, `os.system`, `os.exec*`, `os.posix_spawn`, `os.spawn*`, `os.fork`, `os.forkpty`,
`pty.spawn`, `socket.connect`, `socket.bind`), `:114` (`c.run` wraps every tool call in `hook.py`),
`:244-256` (REAL copies the five hash-pinned captures to `real/*.doc`, renders the oracle with
`soffice --headless --convert-to "txt:Text (encoded):UTF8"` under a private profile), `:302` (per-leg < 2
→ exit 2). `round52/c1-count.py:215` invokes the tool *without* the hook (REGRESS leg).

Ran, delegating forge (`sha256 9c8def9b582dccf2e33869d4fcda455c170175d8ae5bdc2a9bded7165887d6cd`,
renders the capture with `soffice` and prints its text):

```
$ python3 corpus/evidence/round54/c1-count.py --tool $S/ctl/delegate.py --seed 97 --per-leg 2 --work $S/c1forge
tool=.../delegate.py sha256=9c8def9b... seed=97 per-leg=2
GEN=FAIL ggen0.doc rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'
NONWORD=FAIL x0.xls rc=97 err=b'AUDIT_FORBIDDEN subprocess.Popen\n'
ENCRYPTED=FAIL genc0.doc rc=97 err=b'AUDIT_FORBIDDEN subprocess.Popen\n'
MALFORMED=FAIL gmal0.doc rc=97 err=b'AUDIT_FORBIDDEN subprocess.Popen\n'
REAL=FAIL 54fe0734c01f699e735b4b0a rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'
REGRESS=FAIL r52 ['LEGS=1/9'] ['SUPPLEMENT_LEGS=0/4']
LEGS=0/6
C1=FAIL
exit=1
```

Ran, the landed tool at the same seed (hook transparent to a non-delegating tool; REAL judged by the
counting-time oracle):

```
$ python3 corpus/evidence/round54/c1-count.py --seed 97 --per-leg 2 --work $S/c1honest
tool=.../tools/capture-text.py sha256=fd0ed3f58565b781ab8eedaad5d229976e150bdd8e391a2b0cacd0a0825fcd89 seed=97 per-leg=2
GEN=PASS 2 docs
NONWORD=PASS 2 sheets
ENCRYPTED=PASS 2 docs
MALFORMED=PASS 2 docs
REAL=PASS 5 captures
REGRESS=PASS r52 ['LEGS=9/9'] ['SUPPLEMENT_LEGS=4/4']
LEGS=6/6
C1=PASS
exit=0
```

```
$ python3 corpus/evidence/round54/c1-count.py --per-leg 1
usage: --per-leg must be at least 2 (sample-size guard)
exit=2
```

## 99 — a handoff is "dispatched" only with the dispatcher's marker or a results file

Ran:

```
$ for f in .ufo/waves/round-53/w2.ready.dispatched .ufo/waves/round-53/w2-results.json \
          .ufo/waves/round-54/w1.ready.dispatched; do
    [ -e "$f" ] && echo "PRESENT $f" || echo "ABSENT $f"; done
ABSENT .ufo/waves/round-53/w2.ready.dispatched
ABSENT .ufo/waves/round-53/w2-results.json
ABSENT .ufo/waves/round-54/w1.ready.dispatched
$ cat .ufo/waves/round-53/w2.ready
{"lane":"chousa","round":53,"wave":"w2","dispatch":".../round-53/w2-dispatch.json","l1":"ChousaR53"}
$ grep -n "W2" /home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md | head -1
14:- **Waves.** W1: 49 seats; 49/49 results, no error field. ... W2: 43 seats dispatched; ... **W2 WAVE-DONE/results had not arrived by the user's wrap directive; ...**
$ python3 -c "import json;d=json.load(open('.ufo/waves/round-53/w1.ready.dispatched'.split(chr(10))[0]))" # (2-line marker: ts + id map)
.ufo/waves/round-53/w1.ready.dispatched lines= 2 ids= 49 mtime= 2026-10-26T21:03:41
.ufo/waves/round-53/w1-results.json seats=49 results=49
$ grep -n "orphan" /home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run9.md
126:... | r53 admitted ...; defects routed incl. w2 results never arrived, counter forgeable 5 rounds; ... w2.ready orphaned - L1 exited before dispatcher marked wave) | r54 in flight ...
```

The wave that ran: marker with 49 ids + `w1-results.json` 49/49. The wave that did not: `w2.ready`
(readiness record naming the dispatch file) only — no marker, no results — reported as "43 seats
dispatched". Live at observation: round-54 W1 has `w1.ready` (154 B, 22:31:41) and `w1.ready.partial`
(43 ids, 22:38:19) and no marker/results; the dispatch file lists 49 seats.

## 100 — a held row's `used-by` updated old→new when an admitted entry cites it

Ran (scratch root `$S/lane` = lane `corpus/SOURCES.md` copy + one entry; `c2-count.py --root`):

```
A) entry: "source: S101 — https://jc.hit.edu.cn/.../1f6f2731-...doc", row used-by unchanged
   HELD_CITED=- HELD_BAD=1
   REF_ID_UNBOUND=2
   C2=FAIL
B) same entry + row used-by cell: "...citation-count-semantics-r37.md, corpus/knowledge/source-type-taxonomy-r37.md"
   HELD_CITED=S101 HELD_BAD=0
   REF_ID_UNBOUND=0
   C2=FAIL            (other C2 legs fail: no quote, span, lesson, new rows — as expected in scratch)
C) used-by updated + "source: S090 — <url>"
   HELD_CITED=- HELD_BAD=1
   REF_ID_UNBOUND=2
   C2=FAIL
```

This is the TOOLED control's red-before reproduced from the lane's own registry:
`controls/c2-controls.txt` prints `BOUND=3/3 … HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=3` for
mechanically bound entries. The registry fact behind it: `corpus/SOURCES.md:111` cell 12 is
` corpus/knowledge/citation-count-semantics-r37.md ` — the entry that will cite S101
(`source-type-taxonomy-r37.md`) is *not* in it, so binding alone cannot pass.

## Draft — to append to `corpus/QUALITY.md` after criterion 96

```corpus/QUALITY.md
97. **A binary capture's text form is a defined, named reading — a tool and a written rule — never a raw decode, and an anchor offset names the form it indexes.** S101's Registry row anchors six quotes in "UTF-16LE text of the raw `.doc` capture" (`corpus/SOURCES.md:111`; the same six in `corpus/lessons/round-49.md:95-100`), and that form is the container's bytes decoded as text: `6dc68fd6b32ce9c8dfcebce8.raw` gives 64,512 characters with 263 U+FFFD and 18,242 control characters, and it is not the document (the `.txt` sidecar holds none of the six phrases — `find` → −1). The defined OLE form (`tools/capture-text.py`; docstring rule: CFB sector chains, FIB wIdent/nFib, Clx piece table, cp1252/UTF-16LE pieces, main story CP 0..ccpText, field results only) gives 27,012 characters, 0 U+FFFD, 0 control characters, and the same six phrases locate exactly once at 11,972 / 12,007 / 12,963 / 12,795 / 14,049 / 25,123 against stated 11,170 / 11,205 / 11,993 / 12,161 / 13,247 / 34,374 — drift +802, +802, +970, +634, +802, −9,251, so no constant repairs an old anchor (all ran). Check: for every `char N` an entry, Registry row or lesson states for a binary capture, the stated form is a named tool+rule and `python3 tools/capture-text.py <raw> --locate '<quote>'` prints `LOCATED count=1 offset=N` with N equal to the stated `char N`; a form that decodes the file's bytes fails the check even when its number reproduces in that decode. Shown able to fail (ran): the S101 row and round-49 rows give 0/6 matches, and `corpus/evidence/round54/build-spans.py:107-113` still returns that decode for a non-zip raw, so a span built from an OLE `.doc` would index it. Named limits: a manual per-anchor check, not a counter; it binds anchors written after the criterion (the six S101 anchors stay wrong until the correction rows land, and a bound row's `anchor` cell is the counter-checked instance, not a lesson table). — `corpus/lessons/round-54.md` `## Mistakes` row 2 (anchor in an undefined form); QUALITY 87.
98. **A frozen capability counter judges real inputs against an oracle computed at counting time from the same bytes by an independent reader, and refuses a tool that delegates to that reader.** The round-54 C1 counter copies the five hash-pinned `.raw` captures to `real/*.doc` (a digest mismatch is `ENV_CHANGED` exit 2), renders them with `soffice --headless --convert-to "txt:Text (encoded):UTF8"` under a private profile at counting time (`corpus/evidence/round54/c1-count.py:244-256`), then holds the tool's whitespace-free text form to every oracle line (≥ 8 non-space characters), a 0.90-1.10 length ratio and two pinned quotes located exactly once in its own stdout (`:259-278`); every tool invocation goes through `hook.py` (`:114`), which aborts with `AUDIT_FORBIDDEN <event>` and exit 97 on `subprocess.Popen`, `os.system`, `os.exec*`, `os.posix_spawn`, `os.spawn*`, `os.fork`, `os.forkpty`, `pty.spawn`, `socket.connect` or `socket.bind` (`:70-76`). Check: `python3 corpus/evidence/round54/c1-count.py --tool <candidate> --seed N --per-leg 2` — a candidate that renders with LibreOffice fails every hooked leg while the landed tool passes REAL. Shown able to fail (ran): a forge that shells to `soffice` and prints its text (sha256 `9c8def9b…`) gives `GEN=FAIL ggen0.doc rc=97 b'AUDIT_FORBIDDEN subprocess.Popen\n'`, `REAL=FAIL … rc=97`, `LEGS=0/6 C1=FAIL` exit 1, and the SHELL control's receipt says the same (`corpus/evidence/round54/controls/c1-controls.txt`); the landed tool at `--seed 97 --per-leg 2` gives `REAL=PASS 5 captures`, `LEGS=6/6 C1=PASS` exit 0. Named limits: the hook covers Python audit events in the tool's own process, not a compiled extension that renders without one; the REGRESS leg re-runs the round-52 counter, which invokes the tool directly (`corpus/evidence/round52/c1-count.py:215`), so a delegating tool can pass REGRESS and still fail the five hooked legs; the oracle is one LibreOffice version, so an environment change fails REAL rather than skipping it (QUALITY 96's sample guard is what keeps a run from being vacuous). — round-53 closure §6 item 6 (frozen-counter forgeability, RW-1); QUALITY 90.
99. **A wave handoff is reported as dispatched only with the dispatcher's marker (`<round>/<wave>.ready.dispatched`) or the wave's results file; otherwise it is reported as not dispatched, whatever the dispatch file, spec or seat roster says.** Round 53 wrote `.ufo/waves/round-53/w2.ready` (a readiness record naming `w2-dispatch.json`) and filed "W2: 43 seats dispatched" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-53/chousa.md:14`), while `w2.ready.dispatched` and `w2-results.json` do not exist (`ls` → both absent, ran) and the orchestrator's run file records "w2.ready orphaned - L1 exited before dispatcher marked wave" (`/home/vgpnk/Projects/shokunin/.scratch/goal-20261026-hyaku-run9.md:126`). Check: for each wave a report calls dispatched, print the marker and the results file — round-53 W1: `w1.ready.dispatched` exists (timestamp + 49 ids) and `w1-results.json` holds 49 seats / 49 results; round-53 W2: marker and results file both absent — and the report sentence must match what was printed. Shown able to fail (ran): the round-53 report line above against the two absent files. Named limits: a `<wave>.ready` record, a `<wave>-dispatch.json`, a `<wave>.ready.partial` roster or a live seat are not dispatch evidence (at draft time round-54 W1 had `w1.ready`, a 43-id `w1.ready.partial` and no marker, so its report must not call W1 dispatched unless the marker or `w1-results.json` exists at filing); the criterion checks the label, not whether the seats then ran well. — `corpus/lessons/round-54.md` `## Mistakes` row 1 (unverified handoff described as pending); round-53 closure §6 item 2; QUALITY 94.
100. **A held registry row's `used-by` is updated old→new when an admitted entry cites it, and the counter fails until it is.** S101's row carries `used-by` = `corpus/knowledge/citation-count-semantics-r37.md` (`corpus/SOURCES.md:111`), and the round-54 C2 controls show mechanical binding leaves it stale: the TOOLED control prints `BOUND=3/3 (min 2) … HELD_CITED=- HELD_BAD=1 … REF_ID_UNBOUND=3` (`corpus/evidence/round54/controls/c2-controls.txt`) with entries that cite the HIT `.doc`. Check: `python3 corpus/evidence/round54/c2-count.py [--lane-only]` prints `HELD_CITED=<id> HELD_BAD=0` only when every entry whose text carries `source: S101 — <HIT url>` is also named in the row's `used-by` cell, and the lesson records the cell's change old→new. Shown able to fail (ran): in a scratch root holding the lane's `SOURCES.md` and one such entry, `--lane-only` prints `HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=2 C2=FAIL`; adding the entry to the cell prints `HELD_CITED=S101 HELD_BAD=0 REF_ID_UNBOUND=0`; with the cell updated but the line mis-numbered `source: S090 — <url>`, `HELD_CITED=- HELD_BAD=1 REF_ID_UNBOUND=2`. Named limits: `HELD_BAD` counts held ids cited without the update, not the lesson's sentence; an entry naming the HIT URL in prose but not on a `source:` line is not a held citation; the counter reads the row from `--root`, so a scratch copy can be probed without touching the lane registry. — round-53 closure §6 item 6 (a counter a mechanical rewrite cannot satisfy); QUALITY 92.
```

## Findings (reported, not patched)

1. **Criterion 99 bites immediately.** At 22:38:19 round-54 W1 had `w1.ready` + `w1.ready.partial`
   (43 ids) and **no** `w1.ready.dispatched` and no `w1-results.json`, while the dispatch file lists 49
   seats and 49 seats are live. If the round-54 report calls W1 dispatched, it needs the marker (or
   results) written by the dispatcher; a partial roster is not it.
2. **The REGRESS leg is outside the audit hook** (`round52/c1-count.py:215` invokes the tool with plain
   `subprocess.run`). A delegating tool passes REGRESS and fails the five hooked legs; the hook is not a
   lane-wide ban.
3. **Two records of S101's `used-by` disagree.** The Registry row names only
   `corpus/knowledge/citation-count-semantics-r37.md`; `corpus/lessons/round-49.md:158` also names
   `corpus/knowledge/source-type-taxonomy-r37.md`. Criterion 100's "old" value is the row's cell, so the
   lesson's copy must not be used as the pre-state.
4. **`build-spans.py` still indexes the UTF-16LE decode** for a non-zip `.raw` (`:107-113`). C2 holds
   S101 (no round-54 span on it), so this round is unaffected, but criterion 97 binds the moment an OLE
   `.doc` enters `quotes.tsv`.
5. **The two entries are not in the lane yet** (`ls corpus/knowledge/source-type-taxonomy-r3*` → no such
   file), so the lane's C2 counter would read `ENTRIES=0/2` if run now; that is the other seats' work,
   not a measurement I made.
6. **Criterion 100 has no exact routed item.** The round-53 closure's six items do not cover a held row's
   `used-by`; the closest is item 6 (a counter a mechanical rewrite cannot satisfy), which is what the
   draft cites. I did not invent a Mistakes row: the Mistakes seat's plan carries three rows and none is
   this defect. If the L1 wants a precise pointer, the round-54 `## Gate` held decision for S101 or a new
   Mistakes row is the place.
7. **Row numbers 1 and 2 in criteria 97 and 99 are the Mistakes seat's enumeration, not yet a file**
   (`.ufo/waves/round-54/w1-spec.json`, `R54DraftMistakes`: (1) unverified handoff described as pending,
   (2) anchor in an undefined form, (3) round-53 W2 registry uncommitted). `corpus/lessons/round-54.md`
   does not exist at this seat's observation; the L1 must reconcile the numbers on integration.

## Scope notes

- Read-only outside the report: no lane file, no git/jj state, no `/home/vgpnk/Projects/shokuknow`
  write, no campaign tool run, no network, no pacman, nothing written to a PATH directory. No tool
  installed or upgraded.
- The C1 counting runs above are check receipts (`--seed 97 --per-leg 2`), not the claim's measurement;
  C1/C2 admission stays with the frozen counters on the landed commit.
- Scratch removed after the receipt text above was copied here; `pgrep -u $USER -f
  "UserInstallation=file://$S"` printed nothing, and no `soffice.bin` survived.

VERDICT: drafted QUALITY criteria 97-100 with each check run both ways — S101's six anchors mismatch the defined form 0/6 (raw decode: 64,512 chars/263 U+FFFD/18,242 controls vs 27,012/0/0), a delegating forge is refused `AUDIT_FORBIDDEN` `LEGS=0/6` while the landed tool prints `LEGS=6/6`, round-53 W2's "43 seats dispatched" has no marker or results, and `HELD_BAD` goes 1 → 0 only when S101's `used-by` cell gains the citing entry — and reported the live round-54 W1 marker gap, the unhooked REGRESS leg, the stale round-49 `used-by` copy and the UTF-16LE fallback in `build-spans.py`.
