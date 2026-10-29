# MutC1V2Legs — mutation test of c1v2-count.py (legs, snap, tree_of, golden) against the frozen battery

Item: mutation-tester, round 62 chousa, wave w1. Lane root `/home/vgpnk/Projects/shokunin/chousa-shokunin`.
Frozen counter `corpus/evidence/round62/c1v2-count.py` sha256 prefix `b7016fba91b03460` (matches the claim's
after-target); battery `c1v2-battery.py` prefix `9afe00b917fb95e2`. Claims file sha256 `a3193ebd328919e2…` as frozen.
No frozen file was edited. Only write: this report. Scratch `/fast/scratch/hyaku/chousa-r62/MutC1V2Legs/` (deleted at yield).
No tool installed or upgraded.

## Findings

1. **The battery kills 2 of 20 leg-level mutants, and neither kill is a leg-level detection.** M16 (drop the P03
   NOPYC check) is caught only because forger F12 is then accepted (11/12). M19 (golden `tree_of` drops parent
   directories) breaks the landed builder (LANDED 0/3, POSITIVES 0/4): a false-negative kill, not a forger kill.
2. **17 of 18 survivors are real control gaps.** Each one has a named builder that the intact counter rejects
   (per-leg FAIL) and the mutant accepts (per-leg PASS). The frozen battery has no subject that isolates any single
   leg, so the leg is invisible to BATTERY=PASS. One survivor (M05) is equivalent.
3. **Cause, measured:** every neutral-profile forger fails 9–11 legs under the intact counter (base builder:
   `LEGS=11/20`, failing P03, H07–H13, H16), so no forger depends on one leg. Weakening any one leg therefore
   changes no forger verdict. The 12/12 is redundancy-saturated, not leg-by-leg coverage.
4. **Witness builders are routed as counter limits, not refutations** (claims.md: forgers beyond the twelve are
   counter limits for the next battery). They are authored in this wave; overfit risk is the same as the claim's
   named limit on the forgers.
5. **Operability note (measured):** the sandbox makes the builder PID 1 of `unshare -p`. A builder that sends itself
   SIGKILL is ignored (kernel rule for init in a PID namespace), so a self-kill witness did not fire until
   replaced by `os._exit(3)`. The counter's exit-code checks are therefore the only way a builder can end abnormally.
6. **Calibration:** battery wall time was 107–254 s per run with four runs in parallel on a 32-core host at load
   ~12 (`uptime` 12.44 before the run). The claim's "about 50 s" is the quieter-host figure. Not separately measured.

## Method

- Driver (scratch only): `/fast/scratch/hyaku/chousa-r62/MutC1V2Legs/drive.py`, run `python3 -B drive.py`
  (total 1198 s). Each mutant is a copy of the frozen counter with one edit (`str.count(old) == 1` asserted, then
  `compile()`), placed at `<scratch>/mut/<M>/corpus/evidence/round62/c1v2-count.py` with a copied
  `tools/capture-text.py`, so the counter's LANE is the copy. Battery run per mutant:
  `python3 -B <lane>/corpus/evidence/round62/c1v2-battery.py --counter <scratch>/mut/<M>/corpus/evidence/round62/c1v2-count.py --work <scratch>/bat/<M>`
  (the `--landed` default is the lane's `tools/build-spans.py`). KILLED = battery exit 1; SURVIVED = exit 0.
- Control M00 (no edit) and the lane counter run directly both print
  `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS` (exit 0). The copy layout
  reproduces the frozen result.
- Witnesses: each survivor's edit is run against a builder that isolates the leg, with the intact counter and the
  mutant, comparing `LEG` lines (`python3 -B <counter> --builder <W> --work <fresh>`). Witness sources are
  `/fast/scratch/hyaku/chousa-r62/MutC1V2Legs/wit/*.py` (deleted at yield; the edit is reproduced below).
- Two witnesses first failed to fire: Wt-kill (self-SIGKILL, see finding 5) and Wt-hang (the trigger string
  never appeared because capture-text refuses the 70 MB form before the length check). Both were corrected and
  rerun (`wit2.py`, output below). No other rerun.

## Mutant table (20 new mutants; X01–X12 not repeated)

Battery verdicts are full-battery runs (`--only` not used). "Forgers accepted" lists any F-subject battery MISS.

| ID | Edit on the frozen counter | Battery (exit, verdict) | Forgers newly accepted | Class | Witness (intact vs mutant leg) |
|---|---|---|---|---|---|
| M01 | `snap()` ignores mtime everywhere (`mtime = False`) | 0, SURVIVED (BATTERY=PASS) | none | GAP | Wt-touch: H07, H09, H11, H12 intact fail → mutant pass |
| M02 | P01 compares `snap(..).keys()` only (content dropped) | 0, SURVIVED | none | GAP | Wt-content: P01 fail → pass |
| M03 | P04 `r2["rc"] == 1` → `!= 0` | 0, SURVIVED | none | GAP | Wt-check2: P04 fail → pass |
| M04 | H17 `rc in (1, 2)` → `!= 0` | 0, SURVIVED | none | GAP | Wt-kill: H17 fail → pass |
| M05 | H18 drops `not timeout` | 0, SURVIVED | none | EQUIVALENT | none: `timeout` is `rc == -9`, excluded by `rc in (1, 2)` |
| M06 | H10 drops `unchanged and` | 0, SURVIVED | none | GAP | Wt-exit1-base: H10 fail → pass |
| M07 | H11 victim mtime skipped | 0, SURVIVED | none | GAP | Wt-touch: H11 fail → pass |
| M08 | H12 victim mtime skipped | 0, SURVIVED | none | GAP | Wt-touch: H12 fail → pass |
| M09 | `RSS_LIMIT_KIB` 96 → 256 MiB | 0, SURVIVED | none | GAP | Wt-read150: H14, H15 fail → pass |
| M10 | H16 `rc == 2` → `!= 0` | 0, SURVIVED | none | GAP | base builder (exits 1 on H16): H16 fail → pass |
| M11 | H19 drops `clean_out` | 0, SURVIVED | none | GAP | Wt-partial: H19 fail → pass |
| M12 | H13 drops `not leaked` | 0, SURVIVED | none | GAP | Wt-leak: H13 fail → pass |
| M13 | H07 both refusal-snapshot compares without mtime | 0, SURVIVED | none | GAP | Wt-touch: H07 fail → pass |
| M14 | H09 refusal-snapshot compare without mtime | 0, SURVIVED | none | GAP | Wt-touch: H09 fail → pass |
| M15 | H08 `ok8` keeps exit 0, drops tree compare | 0, SURVIVED | none | GAP | Wt-noreplace: H08 fail → pass |
| M16 | P03 `ok3 = tools_unchanged(fx)` → `True` | 1, **KILLED** (FORGERS 11/12) | F12 | KILLED (forger) | — |
| M17 | P05 `rc == 1` → `!= 0` | 0, SURVIVED | none | GAP | Wt-exit2: P05 fail → pass |
| M18 | H20 drops `not timeout` | 0, SURVIVED | none | GAP | Wt-hang: H20 fail (timeout) → pass |
| M19 | `tree_of` drops parent-directory entries | 1, **KILLED** (LANDED 0/3, POS 0/4) | none (false negatives) | KILLED (false neg.) | — |
| M20 | `big_leg` drops the RSS clause | 0, SURVIVED | none | GAP | Wt-read150: H14, H15 fail → pass |

Counts: n = 20, KILLED = 2 (M16 forger kill, M19 false-negative kill), SURVIVED = 18, of which equivalent 1 (M05)
and control gaps 17.

## Witness builders (all in scratch; edit against the landed `tools/build-spans.py` unless marked base)

- Wt-touch: after `a = ap.parse_args()`, `os.utime` on every regular file under `--out` (rglob, follows links).
- Wt-content: `files[name] = span.replace(" ", "_", 1)` (same byte length, different content).
- Wt-check2: `--check` exits 2 when stale (`else 2`).
- Wt-kill: `Forms._open` ends an unreadable capture with `os._exit(3)`.
- Wt-exit1-base (base): `sys.exit(main() or 1)`.
- Wt-read150: reads 150 MiB of each cache file into memory before anything else.
- Wt-partial: creates `--out` and writes `partial.txt` before reading quotes.
- Wt-leak: copies each cache `.txt` (through the symlink) to `--out/leak.txt` before reading quotes.
- Wt-noreplace: `--replace` keeps the stale files (`os.unlink` removed).
- Wt-exit2: refused rows exit 2.
- Wt-hang: sleeps 999 s when a cache `.raw` zip over 32 KiB exists (H20 only).

## Evidence (commands and observed output)

- Claim digest: `sha256sum corpus/evidence/round62/claims.md` → `a3193ebd328919e2…` (matches the frozen value).
- Intact counter on the base builder: `python3 -B corpus/evidence/round62/c1v2-count.py --builder corpus/evidence/round62/controls/base-build-spans.py --work <scratch>/base-run`
  → `LEGS=11/20 C1V2=FAIL`; failing legs P03, H07, H08, H09, H10, H11, H12, H13, H16.
- Lane counter through the battery (control): `… c1v2-battery.py --counter <lane counter> --work <scratch>/bat/LANE`
  → `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=PASS`.
- M00 (copy, no edit): same line, `BATTERY=PASS`.
- M16 battery: `FORGERS_REJECTED=11/12 BATTERY=FAIL`, `SUBJECT FORGER F12 … counter_exit=0 want=1 MISS`.
- M19 battery: `LANDED=0/3 POSITIVES=0/4 FORGERS_REJECTED=12/12 STUBS_REJECTED=4/4 BATTERY=FAIL`.
- Witness rerun (`wit2.py`, 130 s):
  `WIT ('INTACT','Wt-kill') exit 1 | LEGS=19/20 C1V2=FAIL`, `WIT ('M04','Wt-kill','mut') exit 0 | LEGS=20/20 C1V2=PASS`,
  `DIFF M04 Wt-kill ['H17 UNREADABLE'] intact fail mutant pass`;
  `WIT ('INTACT','Wt-hang') exit 1 | LEGS=19/20 C1V2=FAIL`, `WIT ('M18','Wt-hang','mut') exit 0 | LEGS=20/20 C1V2=PASS`,
  `DIFF M18 Wt-hang ['H20 BIGFORM'] intact fail mutant pass`.
- Witness sweep (first run, `drive.py`): the other 15 DIFF lines are listed in the table; each shows exactly the
  named leg(s) differing and no others (e.g. `DIFF M01 Wt-touch ['H07 FOREIGN','H09 ORPHAN','H11 FILELINK','H12 TSVLINK']`).
- Self-kill observation: first Wt-kill (`os.kill(os.getpid(), SIGKILL)`) gave `rc=1` and the refusal line
  `build-spans: refused S100: …txt unreadable (Permission denied)`; the builder ran as `uid=65534(nobody)` inside
  `unshare -Ufp`, and the self-signal was ignored (init of its PID namespace).

## Gap list for the next battery (routed, not a refutation of C1)

Each gap needs one isolated subject per leg (one witness per row above) to reach a battery verdict. The witnesses
are the candidate subjects: Wt-touch, Wt-content, Wt-check2, Wt-kill, Wt-exit1-base, Wt-read150, Wt-partial,
Wt-leak, Wt-noreplace, Wt-exit2, Wt-hang, plus the base builder for M10. M05 needs no subject.

## Named limits of this item

- Witnesses are authored by this seat (overfit risk, as for the battery's own forgers); no external builder was used.
- One mutant per leg; combinations not run. Equivalence of M05 is argued from `run()`'s `timeout = rc == -9`, not
  from a counterexample search.
- Battery verdicts are on this host (one kernel, x86_64, unprivileged userns); the H17 mode-000 check ran as
  `nobody` inside the sandbox.

VERDICT: KILLED=2/20 survivors_that_are_gaps=17
