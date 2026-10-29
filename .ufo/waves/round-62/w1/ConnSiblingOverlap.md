# ConnSiblingOverlap — round 62, wave w1 (connector)

Read-only scan of 21 sibling lanes (`/home/vgpnk/Projects/shokunin/*-shokunin`, excluding nothing; chousa included as own-lane context) over `PROVINCE.md`, `corpus/knowledge/`, `corpus/SOURCES.md` and `tools/`. No lane file written, no git call, no scratch created, no tool installed. Scope question: does any sibling already hold knowledge on (a) kernel path-resolution flags, (b) namespace sandboxing as a test harness, (c) forger or do-nothing batteries for counters?

## Findings

1. **C2 (openat2): no sibling holds kernel path-resolution flag knowledge.** `openat2` as a token appears only in tameshi's syscall tracer and its source register (R1). No `RESOLVE_*` flag appears in any sibling knowledge, province or source file; the only `RESOLVE_` hits are unrelated (`XKB_ERROR_CANNOT_RESOLVE_RMLVO`, mado `xkb-keymap-compile-r48.md:66`; `RESOLVE_ATTRS` AST names, kotodama `receipt_guard_adoption.py:70`). The openat2 entry is therefore complementary, not duplicate, on the kernel-semantics axis.

2. **C2 overlaps the fleet's userspace answer, which is widespread.** Six lanes implement `O_NOFOLLOW` per-component walks or descriptor-relative opens (R4–R6). Souji's own code states the gap that `RESOLVE_BENEATH`/`RESOLVE_NO_SYMLINKS` would close in the kernel: a parent directory swapped after the guard (R4, `souji-worktree-drift.py:241-242`; `souji-cert-evidence.py:146-147`). The openat2 entry should cite these as the userspace precedent it supersedes or complements; none of them is kernel-enforced.

3. **Contested ground: souji origin-record entries (round-61 naming confirmed, with one correction).** Round 61 named souji's origin-record entries as contested for atomic record writing (`corpus/lessons/round-61.md:74`). The round-62 openat2 entry does not write records and does not enter that ground. The live overlap is in chousa's own round-61 entry `corpus/knowledge/derived-output-safety-r61.md`, Claims 2–4 (lines 29–31: `O_EXCL` fails on a symlink; `rename` overwrites a planted link; atomic replace). Those facts duplicate souji's `origin-record-exclusivity-r28.md` (S212 `open()` exclusive creation, S213 `rename()` atomicity, lines 15–22 and 52–54) and the round-61 entry cites none of souji's rows (grep for `souji|origin` in that file returns no hit). This is duplicate-by-fact, uncited; it is not contradicted by souji.

4. **C1 (counter batteries): the forger/do-nothing method has precedents; no sibling was found holding a harness-detecting forger battery.** Do-nothing and forged-receipt controls appear in kake, kumitate, kotoba and kaidoku (R9). Sandboxed counters using bwrap appear in mado, kengaku, tameshi, kake and mori (R8). A search for evasion/sniff/harness-aware/reward-hack terms in knowledge found nothing that builds a counter-detecting forger battery (R9–R11 are the closest). This is a negative search, not an exhaustive audit [INFERENCE on absence].

5. **C1's namespace choice diverges from the fleet's primitive, and the divergence is named by siblings.** Kumitate's routing row says a counter runs under bwrap with `env -i` as the immediate parent (R7). C1 uses `unshare -Ufp --kill-child --mount-proc` (`c1v2-count.py:141`). Kumitate also says the sandbox is not a security boundary (`agent-isolation-substrates.md:188`). Tsukuroi's `PROVINCE.md:234-236` records the same limit C1 names: a census that detects its namespace and behaves honestly only there cannot be told apart. This complements C1's named limit (NSpid / `getpid()==1` not stopped).

6. **In-lane divergence (not C1, noted for L1).** C1's counter fails closed when `unshare` is unavailable (`c1v2-count.py:681-684`), as mado does (`mado-shokunin/quality/counters/c1-r40-live-v2.py:496`, SETUP exit 2). Chousa's `tools/research-gate.sh:6149-6160` skips the namespace cases by name on the same condition. Both are defensible; they are different policies on the same host.

7. **Tool note (recorded).** The `_grep` tool does not expand a wildcard inside an absolute path (`/home/vgpnk/Projects/shokunin/*-shokunin/...`). Control: `bwrap|bubblewrap` over `*-shokunin/PROVINCE.md` returned `No matches found`, while `kengaku-shokunin/PROVINCE.md:272` contains `bubblewrap`. Every "No matches" from the first `_grep` batch is therefore void; all counts below come from `bash` `grep -rIlE`/`grep -rInE`. Filed as a tool issue.

## Overlap table (k = 11)

Relation key: DUP = duplicates, CON = contests, COMP = complements, DIV = diverges (no contradiction).

| # | Lane | Evidence (path:line) | Overlap | Rel. to |
|---|---|---|---|---|
| R1 | tameshi | `tools/trace-inputs.py:75,95,97,384`; `corpus/SOURCES.md:84,115` | `openat2` in the traced syscall set; path argument at index 1, dirfd at 0 (argument positions only, no `RESOLVE_*` semantics) | C2 — COMP |
| R2 | souji | `corpus/knowledge/origin-record-exclusivity-r28.md` (S212/S213, lines 15–22, 52–54); `origin-record-durability-r28.md`; `origin-record-writer-r27.md` | exclusive creation, atomic publication, durability of an origin record | C2 (via R3) — CON (named by round 61) |
| R3 | chousa (own) | `corpus/knowledge/derived-output-safety-r61.md` Claims 2–4, lines 29–31; Q3/Q4 lines 17–18 | `O_EXCL` on symlinks and `rename` over a link — same facts as R2 | C2 — DUP (uncited) |
| R4 | souji | `tools/souji-evidence-cache.py:112-120,564-593,620`; `tools/souji-worktree-drift.py:236-263`; `tools/souji-cert-evidence.py:146-147` | per-component `O_NOFOLLOW` walk; documented parent-swap limit | C2 — COMP (userspace; kernel openat2 would supersede) |
| R5 | mori | `tools/mori-seat-terminal.py:12-30` | `O_DIRECTORY|O_NOFOLLOW` descriptor-relative walk of child directories | C2 — COMP |
| R6 | kumitate / kama / kaidoku / mado / souji | `kumitate .../route-resolution.md:32`; `kumitate .../local-ship.md:131,152,226` (O_NOFOLLOW deliberately absent for symlinked contracts); `kaidoku tools/round-42/fetch-carrier.py:53-57,263-276`; `kama tools/kama-llamacpp-live.py:344-347`; `mado tools/mado-action-plan.py:151-157` | fleet `O_NOFOLLOW` / `O_EXCL|O_NOFOLLOW` temp-and-rename writers; one lane chooses the opposite on purpose | C2 — COMP / DIV |
| R7 | kumitate | `corpus/knowledge/agent-isolation-substrates.md:164,179-180,188`; `scripts/cap-run.mjs:32` | counters/controls run under bwrap `--unshare-all --die-with-parent` with `env -i` as parent; PID 1 keeps launcher env (M5, lines 110–114); "no security boundary" | C1 — DIV (bwrap vs unshare) |
| R8 | mado, kengaku, tameshi, kake, mori | `mado quality/counters/c1-r40-live-v2.py:19-23,480,496`; `kengaku PROVINCE.md:297-299`; `tameshi corpus/knowledge/guard-kill-closure.md:129`; `tameshi corpus/knowledge/hermetic-env-differential.md:26`; `kake/mori counters cited at kengaku PROVINCE.md:328-331` (cited, not re-read) | bwrap as the test envelope for counters/probes; mado fails closed without bwrap | C1 — DUP (method) / COMP |
| R9 | kake, kumitate, kotoba, kaidoku | `kake corpus/knowledge/receipt-integrity.md:74-84`; `kumitate corpus/knowledge/counter-amendment-discipline.md:30-31,63-65`; `kotoba corpus/knowledge/scoped-rules-counter-round61.md:45-61`; `kaidoku corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md:79` | do-nothing controls and forged-receipt controls; a mutant that fails the same command | C1 — DUP (method); none holds per-harness forger builders |
| R10 | tsukuroi | `PROVINCE.md:217-218,234-236,287-288` | a namespace-detecting census cannot be told apart from an honest one on a constant host; a namespace hiding `/sys` yields a false all-clear | C1 named limit — COMP |
| R11 | kama | `corpus/knowledge/battery-execution-evidence.md:40-47` | in-process audit-hook confinement; "a hostile battery that disarms the hook is not stopped; bwrap/unshare would be needed" (line 47) | C1 — COMP (C1 takes the namespace step kama names) |

Precedent for the scan method itself: kotoba `corpus/knowledge/sibling-overlap-census-round49.md` (not counted in k).

## Calibration of the count

- k counts holdings that touch C1 or C2 topics and were read at the cited line. R8 and R9 are families of 3–5 files each; counting each file would raise k to about 20. The table keeps one row per overlap family.
- `kake c42_count.py`, `kake sealed_count_v2.py` and `mori count-c2-a1.py` are cited only through kengaku's PROVINCE table; I did not re-read them. Their rows are marked as cited.
- I did not read the round-62 wave drafts (`.ufo/waves/round-62/w1/RevC2V2Claim*`) for overlap; the scope was sibling lanes.

## Recorded commands

    cd /home/vgpnk/Projects/shokunin && for l in *-shokunin; do ...; done          # lane surface presence (21 lanes)
    grep -rIlE 'openat2|RESOLVE_(NO_SYMLINKS|BENEATH|IN_ROOT|NO_MAGICLINKS|NO_XDEV|CACHED)|O_NOFOLLOW' -- */PROVINCE.md */corpus/knowledge */corpus/SOURCES.md */tools
    grep -rInEi 'unshare|bwrap|bubblewrap|pid namespace|user namespace|network namespace|CLONE_NEW|setns\(|pivot_root' -- (same paths)
    grep -rInEi 'forger|forgery|forged|anti-?detect|detection (test|battery)|do-nothing|null-(pass|fail|counter|hashlist)|stub (builder|counter)|single-defect|mutant' -- (same paths)
    grep -rIwE 'openat2' -- (same paths);  grep -rIcE 'RESOLVE_[A-Z_]+' -- (same paths)
    grep -rInEi 'evasion|sniff|harness-aware|detects? the (harness|counter|grader|sandbox)|reward.hack|specification gaming' -- (same paths)
    grep -rInE 'kill-child|mount-proc|die-with-parent|setsid|NSpid|getpid\(\) ?== ?1|reaper|pid 1|PID 1' -- (same paths)
    grep -nE '^## Do-nothing reachability' kake-shokunin/corpus/knowledge/receipt-integrity.md   # and similar line checks

Counts: openat2 sibling files = 3 (tameshi tools and SOURCES; kumitate kimi-mcp-plane.md is a `grep -c` text false positive); RESOLVE_ relevant = 0; namespace/sandbox files = see R7–R8; forger/do-nothing files = see R9.

## Not run

- No C1/C2 counter, battery, control or probe was run (not in this seat's assignment).
- No sibling file was edited; no fixture repository was created.

VERDICT: SIBLING_OVERLAPS=11 contested=souji
