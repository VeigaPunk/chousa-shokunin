# R52W2ExecSeedSupplement — flake and independence of the C1 supplement and the frozen counter

seat R52W2ExecSeedSupplement (leaf) · 2026-10-26 · lane `/home/vgpnk/Projects/shokunin/chousa-shokunin`; measured commit `e769c03738d08c36109556ebf301a1db0dcf143d` in a shared clone (`git clone -q --shared … $S/clone`, `checkout -q e769c03…`), `git rev-parse HEAD` = `e769c037…`, `git status --porcelain` = 0 lines. Digests there: tool `81ba0db0…d05277`, `c1-count.py` `4ec29333…101cbaa`, `c1-supplement.py` `86711a5f…c0109b0`. Lane HEAD has since moved to `d1d972c` (w2 spec); every number below is of `e769c03`. Scratch `/fast/scratch/hyaku/chousa-r52/R52W2ExecSeedSupplement`, `TMPDIR` there (never `/tmp`). Lane read only; no pacman (paused host-wide), no install; `time.monotonic` used because `/usr/bin/time` is absent.

## 1. What I attacked, and the result

1. post-freeze supplement `c1-supplement.py` (4 legs), 100 runs — no flake: 100/100 `4/4 PASS`;
2. frozen counter `c1-count.py` (9 legs), 20 runs — no flake: 20/20 `9/9 PASS`;
3. independence — the supplement separates spelling-keyed forges (9/9 → 0/4) but **imports the counter's generators**, so a `w:sdt`-blind tool passes the counter 9/9 and the supplement 3/4 (§5a);
4. the pinned `REAL_TEXT` oracle — re-derived here from `build-spans.docx_text`, matches (§5c).

## 2. Mandated matrix — 20 unseeded + seeds 1..20 supplement, 10 unseeded counter: 50/50 PASS

Driver (28 lines, verbatim; cells = tag, legs, verdict, rc, wall, TMPDIR entry count, leftover `c1supr52-`/`c1r52-` names, `/tmp/c1*52-*` hits, per-leg):

```python
import os, pathlib, re, subprocess, sys, time
S = pathlib.Path("/fast/scratch/hyaku/chousa-r52/R52W2ExecSeedSupplement")
LANE = S / "clone"
SUP = str(LANE / "corpus/evidence/round52/c1-supplement.py")
CNT = str(LANE / "corpus/evidence/round52/c1-count.py")
env = dict(os.environ, TMPDIR=str(S))
def snap():
    ent = sorted(p.name for p in S.iterdir())
    tmpjunk = sorted(str(p) for p in pathlib.Path("/tmp").glob("c1*52-*"))
    return len(ent), [e for e in ent if e.startswith(("c1supr52-", "c1r52-"))], tmpjunk
fails = 0
def run(cmd, tag, legs_re, pass_re):
    global fails
    tb, lb, tjb = snap(); t0 = time.monotonic()
    p = subprocess.run([sys.executable] + cmd, capture_output=True, text=True, env=env)
    dt = time.monotonic() - t0
    ta, la, tja = snap()
    legs = re.search(legs_re, p.stdout, re.M); verdict = re.search(pass_re, p.stdout, re.M)
    legline = " ".join(l.split("=", 1)[0][:4] + "=" + l.split("=", 1)[1].split()[0][:4]
                       for l in p.stdout.splitlines() if "=" in l and not l.startswith(("LEGS", "C1=", "SUPPLEMENT")))
    oklegs = legs and legs.group(1) == legs.group(2)
    print(f"{tag}\tLEGS={legs.group(1)}/{legs.group(2) if legs else '?'}\t{verdict.group(0) if verdict else '?'}"
          f"\trc={p.returncode}\t{dt:.2f}s\ttmp {tb}->{ta}\tleft={la or '-'}\ttmpjunk={tjb or '-'}\t{legline}")
    if not (oklegs and p.returncode == 0):
        fails += 1
        print(f"----- FULL OUTPUT {tag} (argv {cmd[1:]}) -----\n{p.stdout}{p.stderr}----- END {tag} -----")
    return dt
for i in range(1, 21):
    run([SUP], f"sup-unseeded-{i:02d}", r"^SUPPLEMENT_LEGS=(\d+)/(\d+)$", r"^C1_SUPPLEMENT=\w+$")
for n in range(1, 21):
    run([SUP, "--seed", str(n)], f"sup-seed-{n:02d}", r"^SUPPLEMENT_LEGS=(\d+)/(\d+)$", r"^C1_SUPPLEMENT=\w+$")
for i in range(1, 11):
    run([CNT], f"cnt-unseeded-{i:02d}", r"^LEGS=(\d+)/(\d+)$", r"^C1=\w+$")
print(f"ALL={'PASS' if fails == 0 else 'FAIL'} nonpass={fails} runs=50")
```

Observed (`ALL=PASS nonpass=0 runs=50`, rc 0; every supplement row `PREF=PASS RELS=PASS SYNT=PASS REAL=PASS C1_S=PASS`, every counter row all nine legs PASS):

```
sup-unseeded-01 LEGS=4/4 C1_SUPPLEMENT=PASS rc=0 2.35s tmp 3->3 left=- tmpjunk=-   [02–20 identical]
sup-seed-01    LEGS=4/4 C1_SUPPLEMENT=PASS rc=0 2.31s tmp 3->3 left=-             [02–20 identical]
cnt-unseeded-01 LEGS=9/9 C1=PASS rc=0 1.33s tmp 3->3 left=- tmpjunk=-            [02–08 identical]
```

`tmp` rose 3→4→5 between counter runs 08 and 10 because I wrote `mkmut.py`/`mut/` into the same directory **while the matrix ran** (my interference, disclosed). `left=-` in all 50 snapshots, `tmpjunk=-` in all 50. Extended sweep: supplement seeds 21..80 → 60/60 `4/4 PASS rc=0`; counter seeds 21..30 → 10/10 `9/9 PASS rc=0`; zero non-PASS in 100 supplement + 20 counter runs. `--seed 7` twice printed byte-identical stdout, as did every seeded reproduction in §4.

## 3. Clean-room residue, `--work`, timing (nothing else running)

`quiet/` as `TMPDIR`, exact recursive listing (names+sizes) compared per run: 10 runs (supplement seeds 101–105, counter 101–105) all `residue=none`, 0 entries after. `--work $PWD/w2dir` honoured by both (`4/4` and `9/9`, `w2dir entries after: 0` each). `/tmp/c1*52-*`: 0. Single-run wall time: **supplement 2.59 s**, **counter 1.51 s** (matrix 2.22–2.49 / 1.33–1.53; `--per-leg 1` 0.61–0.70 s).
Correction to my own data: the sweep flagged `residue=[c1supr52-vplu7r3w…]` on seeds 44–46 — that dir was my own concurrent `strace` run sharing the TMPDIR, gone at end (`quiet empty at end: True`), not a supplement leak. The `finally: shutil.rmtree` hooks (`c1-supplement.py:168`, `c1-count.py:328`) held in every clean run.

## 4. First non-PASS in full, reproduced by seed

The matrix produced none, so I proved the harness exhibits and reproduces one (scratch mutant / lane control; production untouched). Supplement vs `controls/forge-shape.py --seed 3`, twice, `identical_rerun=True`, rc 1:

```
PREFIX=FAIL g_paras: text differs at 34 (got 86 chars, want 90)
RELS_FORM=FAIL g_paras: rc=2
SYNTAX=FAIL g_paras: rc=2
REAL_TEXT=FAIL rc=0 chars=21
SUPPLEMENT_LEGS=0/4
C1_SUPPLEMENT=FAIL
```

Counter vs `mut/m5-fallback.py --seed 3` (real tool with only the `mc:Fallback` suppression removed), twice, `identical_rerun=True`, rc 1:

```
PARAS=PASS ok / RUNS_ENTITIES=PASS ok / REVISIONS=PASS ok / LAYOUT=PASS ok
ALTCONTENT=FAIL text differs at 58 (got 97 chars, want 67)
MAIN_PART=PASS ok / LOCATE=PASS ok / REFUSE=PASS ok
REAL=PASS rc=0 count=1 locate=(0, 1, 8996) chars=19787
LEGS=8/9
C1=FAIL
```

## 5. Independence — measured, not read

**(a) The supplement shares the counter's generators.** `c1-supplement.py:58` loads the frozen module (`C = _load("r52_c1_count", "c1-count.py")`); its three generated legs compare with `C.text_ok(...)` against packages from `C.g_paras…g_main_part` (`:149-156`), so their `want` oracle **is** the counter's. Measured with `mut/m3-sdt-drop.py` (one edit: a `w:t` with a `w:sdt`/`w:hyperlink` ancestor emits nothing — a violation of claims.md R52-C1 "a `w:t` element emits its text"): counter `LEGS=9/9 C1=PASS`; supplement `REAL_TEXT=FAIL rc=0 chars=18721`, `SUPPLEMENT_LEGS=3/4`. Only `REAL_TEXT` sees it, and only because the pinned NIPH capture holds `w:sdt` ×1 and `w:hyperlink` ×49 (counted in its `word/document.xml`, 1240 `w:p`).

**(b) The supplement does add the power E1 claims.** Same tool-under-test, seed 3, counter → supplement: `forge-shape.py` 9/9 → **0/4**; `naive-tool.py` 4/9 → **0/4**; `cache-txt-tool.py` 0/9 → 0/4; `const-tool.py` 0/9 → 0/4. The E1 hole is closed and the frozen verdict is unchanged (counter still 9/9 on the forge, as E1 states).

**(b2) The re-spelling is exercised, not skipped.** Instrumented wrapper over the module's `respell_prefixes`/`respell_syntax` for seeds 1..20 + 10 unseeded (`--per-leg 1`, all 30 runs `4/4 PASS`): `w:` as default namespace 1–8 respells/run (every run ≥1), CDATA 4–6, typed `w:br` 1, paired `w:tab` 1, comments 5–7, hex→decimal refs 1 in 27/30 (0 when every sampled `w:t` took the CDATA branch). `respell_rels` sampled directly: `<tw7b3pd:Relationships xmlns:tw7b3pd="http://schemas.openxmlformats.org/package/2006/relationships">` with a prefixed `<…:Relationship` child and shuffled attribute order — semantically the same package, which is why the RELS_FORM leg is a spelling test and not a rule change.

**(c) The pinned oracle is the independent reader's text.** Re-derived, not trusted: in the clone, `build-spans.docx_text(pinned .raw)` → `len 19682`, `sha256 = 754aae4266a19af9518a4bb46bcd484078baeb095df048d171cfc8cc2f24b0d9` = `TEXT_SHA` (`c1-supplement.py:47-48`); raw digest `16fc8c55…09763` = `REAL_SHA` (`c1-count.py:47`); counter `REAL=PASS … locate=(0, 1, 8996) chars=19682`. The digest is a **constant** — the supplement never runs `build-spans.py` — so this holds as re-derived once, by me, and in the erratum.

**(d) Read surface** (`strace -f -e trace=openat`, one seeded run, 74 `execve` = parent + 73 tool calls): non-stdlib opens are only `c1-supplement.py`, `__pycache__/c1-count.cpython-314.pyc`, `tools/capture-text.py` (×146 = 73 × 2) and the pinned `…/.qcache/3a8b45977cd111e45e3980a5.raw`. No `build-spans.py`, no `quotes.tsv`/`spans.tsv`, no `corpus/knowledge` file, no staged merge package. Side effect, not repo pollution: the import writes `corpus/evidence/round52/__pycache__/c1-count.cpython-314.pyc`, covered by `.gitignore:3`.

**(e) No drift behind the numbers.** `git diff 37468ead e769c03 -- corpus/evidence/round52/c1-count.py corpus/evidence/round52/claims.md` = empty (counter and claims frozen); `c1-supplement.py` added at `01c17ce`, post-freeze as E1 says; tool `+32/−5` after candidate `804a4537`, matching E2. Caveat: my first `git diff 37468ead…` failed `bad revision`, and the identical command seconds later resolved (`git cat-file -t` → `commit`, 413 bytes) — a transient object-visibility window in the lane repo (likely a concurrent repack), not a missing freeze commit; I assert no defect on one failure.

## 6. Residual risk (bounded, not observed)

- Prefix collision inside one respelled document: 3 prefixes from `26·36⁶ ≈ 5.67e10` → ≲5.3e-11/document, ≈5e-9/run, ≈6e-7 over ~110 runs [INFERENCE, arithmetic]; would surface as a text mismatch, never a pass.
- The supplement has no REFUSE and no `--locate` leg under re-spelling (`:163` calls the tool with the raw only): a tool printing the right text but mis-locating a CDATA/decimal-ref document is untested by it.
- One host, one interpreter, one filesystem; `REAL_TEXT`'s rule coverage is one 19682-char document.

## 7. Files changed, tooling

No lane file created or edited, nothing staged; my only write is this report. Scratch mutants (`mut/m3-sdt-drop.py`, `m4-toplevel-p.py`, `m5-fallback.py`), the drivers, the clone and `strace.log` lived under `/fast/scratch/hyaku/chousa-r52/R52W2ExecSeedSupplement` and were removed at finish (every receipt cited above is pasted in this file). No tool installed or upgraded.

VERDICT: attacked the post-freeze supplement and the frozen C1 counter for flake and independence at `e769c03` — 100 supplement runs (20 unseeded + seeds 1..80) all `SUPPLEMENT_LEGS=4/4 C1_SUPPLEMENT=PASS` and 20 counter runs all `LEGS=9/9 C1=PASS`, seeds byte-reproducible, zero residue, zero `/tmp` writes, 2.59 s / 1.51 s per run; the supplement separates the forge (9/9 → 0/4) and naive control (4/9 → 0/4), and its pinned digest equals `build-spans.docx_text`'s output re-derived here — but it imports the counter's generators, so a `w:sdt`-blind tool still passes counter 9/9 and supplement 3/4; no flake found, one coverage limit and one transient provenance hiccup recorded, nothing edited.
