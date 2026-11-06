# R83ReviewerTool — review of `tools/gate-records.py` at 81b81173f19d175e2b2a6b409b2a496d09d0b258

Scope: C2 kill rules K2, K3, K4 (frozen in `corpus/evidence/round83/claims.md`), tested against the tool's own docstring.
Bytes attacked: `git archive 81b81173f19d175e2b2a6b409b2a496d09d0b258` (sha256 of `tools/gate-records.py`
`d38443769fe7c2ba014ec9d7861c4078cec24d0a193eeadb2cd5222d0d392687`). `git diff 81b8117 aca2a78 -- tools/gate-records.py`
and `git diff 81b8117 -- tools/gate-records.py` (lane worktree) are both empty, so tip and worktree carry the same tool bytes.
Receipts: `.ufo/waves/round-83/w1/R83ReviewerTool/` (index at the end). Drivers: `.../R83ReviewerTool/drivers/driver.py`, `driver2.py`.
Scratch (extract, fixtures, copies) removed before this report.

Reproduce any receipt:
`D=$(mktemp -d -p /fast/scratch/hyaku) && git -C /home/vgpnk/Projects/shokunin/chousa-shokunin archive 81b81173f19d175e2b2a6b409b2a496d09d0b258 | tar -x -C "$D" && python3 -B "$D/tools/gate-records.py" verify --root "$D" --repo /home/vgpnk/Projects/shokunin/chousa-shokunin FILE...`

## Findings

### F1 — K3 FIRES: genuine `rev` record refused with `FAIL PARSE` (quote begins with `"`)

Exact record line (one line, the quote is the blob's line 85 verbatim):

    GATE-RECORD S212 rev=81b81173f19d175e2b2a6b409b2a496d09d0b258 path=tools/gate-records.py line=85 words=2 quote=" ".join(s.split())

Blob line 85 is `    return " ".join(s.split())`. Checked against every docstring check: the line fits the rev form
(`quote=<text to end of line>`, no restriction on the text); REGISTRY (S212 has a row); REV (blob exists at the rev);
LINE (quote occurs in line 85); WORDS (2 tokens); QUOTE_LEN (1..25). It meets every docstring check.

Observed: `GATE_RECORD …/fx2/k3a.md:1 S212 FAIL PARSE` / `GATE_RECORDS files=1 records=1 ok=0 fail=1`, **exit 1**.
Receipt: `k3a-rev-quote-leading-dquote.txt`. Cause: `parse()` contains `if not quote or quote.startswith('"'): return None`
on the rev branch. No docstring check states this rule; PARSE's documented scope is key/value shape, and the quote is a value.
A second record of the same shape (quoting docstring line 2, which starts `"""`) also prints `FAIL PARSE`, exit 1
(`k3a2-rev-quote-docstring-line.txt`, `S213`).

### F2 — K3 FIRES (arguable reading, stated explicitly): genuine `rev` record for a tracked path containing a space

Exact record line:

    GATE-RECORD S212 rev=81b81173f19d175e2b2a6b409b2a496d09d0b258 path=.ufo/waves/round-80/w2/Exec/SubjC2 RECEIPT/SUBJECT_HONEST.md line=1 words=4 quote=# R80ExecC — wave-2

The path is in the commit (`git ls-tree -r --name-only 81b8117` lists it). Blob line 1 is `# R80ExecC — wave-2`, so REV, LINE, WORDS,
QUOTE_LEN and REGISTRY hold by construction; the tool never reaches them because `parse()` splits the head on single spaces
(`tok.split("=",1)` after `head.split(" ")`), so `RECEIPT/SUBJECT_HONEST.md` is a token with no `=`.
Observed: `GATE_RECORD …/fx2/k3b-space-path.md:1 S212 FAIL PARSE`, **exit 1**. Receipt: `k3b-rev-path-with-space.txt`.
The docstring's form is `path=<repo-relative path>` with no spelling restriction, and no docstring check excludes spaces.
Impact on the lane: 7 committed paths contain spaces (6 under `.ufo/waves/round-80/w2/Exec/SubjC2 RECEIPT/`, 1 at
`.ufo/waves/round-33/w1/ExecD5Check/fixtures/names/has space.md`); none of them can be cited in the rev form.

### F3 — K2 HELD (no in-class record printed OK while violating a documented check)

Searched: the frozen 198 derived forgeries plus 15 positives (`g1-battery.txt`: `TOOL=present POSITIVE=15/15 FORGED_REFUSED=198/198
EXPECTED_CODE=198/198 EMPTY_REFUSED=1/1 RC=3/3 GATE_RECORDS_R83=PASS`, rc 0 — context, observed on the landing tree);
a 36-probe matrix with one violation per documented check (`m-*.txt`, `matrix-summary.txt`); the pass-1 probes that were not
fixture-contaminated (`w1`, `w2`, `w3`, `w5`, `w5b`, `w6`, `w7`, `w10`, `w11`, `w12`, `x1`–`x11`, `c3`); and the probes in F4–F6. Every
violation of a documented check was refused with the documented code
except the residual OKs listed in F4 (R1–R4), none of which violates a documented check. See the check table below for per-check reading.

### F4 — residuals (not K2: no docstring check is violated; listed separately, per the instruction)

R1 — **cross-URL under one S-id (most material).** The tool certifies a record whose URL is not the registry row's source.
Exact line (`x-cross-url-same-id.txt`):

    GATE-RECORD S131 url=https://mp.weixin.qq.com/s/nFQlHQTlXx9-H_NPfyyUnQ fetched=2026-10-27T08:48:20Z tier=B decision=admit capture=corpus/captures/712ec7bb981a9669a6921db7.txt capture_sha256=1443b149a9914773… words=12 quote="环境异常 当前环境异常，完成验证后即可继续访问。 去验证 ： ， 。 视频 小程序 赞 ，轻点两下取消赞 在看 ，轻点两"

Observed: `GATE_RECORD …/fx2/x-cross-url.md:1 S131 OK`, rc 0. S131's registry row names only `nmgyyxh.org.cn`; `refetch.tsv` holds
14 URLs under id S131. The capture is a WeChat verification interstitial ("当前环境异常，完成验证后即可继续访问"), and the tool has no
content check. REGISTRY is S-id existence only. In-class by the frozen definition, but not a K2 violation, because the docstring defines no URL-to-registry check.

R2 — **decision on the admit form.** `GATE-RECORD S203 … decision=reject capture=corpus/captures/f2489455cc311a4de981e926.txt …` → `OK`, rc 0 (`w1-admit-decision-reject.txt`).
The docstring template for url/admit reads `decision=<admit|reject>`, but no check constrains it.

R3 — **`capture_sha256` ASCII suffix.** `capture_sha256=31493aa66bfd6625...` → `OK`, rc 0 (`w2-sha-ascii-ellipsis.txt`). Docstring specifies `[…]` (U+2026) only; `SHA_RE` also accepts `...`.

R4 — **non-canonical rev path.** `path=./tools/gate-records.py` → `OK`, rc 0 (`m-T-REV-dot-slash.txt`). git resolves `./` relative to the cwd inside `--repo`, so the meaning shifts if `--repo` is a subdirectory. Not tested with such a `--repo`.

R5 — **working-tree reads, not committed bytes.** The docstring says "reading only committed lane bytes"; the code opens `SOURCES.md`, captures and `refetch.tsv` from `--root` (the working tree). Shown with a copy whose `SOURCES.md` has an uncommitted row `S990`: REGISTRY passed, `FAIL REFETCH` (`x-uncommitted-registry-row.txt`, rc 1); `git show 81b8117:corpus/SOURCES.md | grep -c '^| S990 '` = 0 (`…-committed-check.txt`). Editing those files is out of class by the claims' own text, so this is a docstring-versus-code inconsistency, not a K2 hit.

R6 — **Cf character inside the token** (`GATE-RECORD\u200bS203 …`, ZWSP) is not a record: `GATE_RECORDS files=1 records=0 ok=0 fail=0`, rc 1 (`m-T-ZWSP-token-glue.txt`). This follows the frozen class (`GATE-RECORD` must be followed by whitespace or EOL). Out of class.

R7 — **`GIT_DIR` in the environment overrides `--repo`.** Genuine rev record (`return " ".join(s.split())`, line 85) with `GIT_DIR=<empty fixture repo>`: `FAIL LINE,REV`, rc 1 (`d-gitdir-env.txt`); without it, `OK`, rc 0. Environment trust; not a docstring check.

R8 — **latent: REGISTRY scans the whole file.** `load_registry` ignores section headings. Today every S-id row is under `## Registry` (213 rows; `## Paths`, `## Search log`, `## Leads (unopened)` contain none). A future S-id row in Leads would satisfy REGISTRY.

R9 — **latent: symlinked `corpus/captures`** would pass CAPTURE_PATH (it compares `dirname(realpath)` to `realpath(captures)`, not to LANE). No symlink exists under `corpus/` at 81b8117 (`git ls-tree -r` mode 120000: none). Not exercised in a worktree.

### F5 — K4 HELD for the exit contract on tested inputs; one docstring deviation

Observed exits: 0 only with records ≥ 1 and all OK (positives, R1–R3, F3 boundary cases); 1 for any FAIL line, for an empty file
(`x1-empty-file.txt`), prose-only (`x2`), list-item record (`x10`), mixed OK/FAIL (`x9`), and a bare `GATE-RECORD` at EOF (`x11`: `FAIL PARSE`, rc 1);
2 for missing FILE (`x3`), missing registry (`x4`), missing refetch log (`x5`), no subcommand (`x6a`), bad subcommand (`x6b`), no FILE args (`x7`).
No run printed FAIL with exit 0.

Deviation: the docstring says "2 on usage or I/O error". An unreadable lesson or capture raises an uncaught `PermissionError`:
`c2-lesson-unreadable.txt` (chmod 000 on a lesson) and `c1-capture-unreadable.txt` (chmod 000 on a capture), both **exit 1** with a traceback and no summary line.
Not a K4 hit (non-zero). Invalid UTF-8: a record line with bytes `\xff\xfe` (`c3-invalid-utf8.txt`) → `FAIL CAPTURE_KEY,QUOTE_ABSENT,REFETCH`, rc 1, no crash.
An invalid-UTF-8 garbage row appended to a copy of `refetch.tsv` does not stop a genuine S203 record: `OK`, rc 0 (`x-invalid-utf8-refetch.txt`).

### F6 — purity (K3 harm): HELD

`d-strace-full.txt`: `strace -f` over a full 15-record run (rounds 80–82; `execve, socket, connect, openat, unlink*, rename*, mkdir*, truncate*, chmod, link*, symlink*`):
0 socket/connect calls; 0 mutating syscalls; 13 `execve` = 1 python + 12 `git`; all 12 `git` argv are `cat-file` (`d2-git-commands.txt`:
12 `-C … cat-file` lines, 0 others); 12 write-flag `openat` calls, all on `/dev/null`. `d-tree-diff.txt`: `diff -r` of the scratch tree
against a fresh `git archive` extract is empty (rc 0), so the tool wrote nothing into its inputs. The tool imports only `argparse, hashlib, os, re, subprocess, sys, unicodedata`.

## Per-check reading (docstring vs code)

| Check | Code | Docstring says | Reading |
|---|---|---|---|
| PARSE | `parse()` | fits none of 3 forms (key/value/extra text) | Enforces key set, duplicates, empty values, int/tier/decision/ts/url shape, `quote=` last. **Over-refuses**: rev quote starting `"` (F1); any space in rev path (F2). `decision` not checked against form (R2). |
| REGISTRY | `reg.get(sid)`, first 11-cell row, any section | S-id has no 11-column Registry row, 0–3 leading spaces | Matches the text. Whole-file scan (R8, latent). |
| TIER | `regrow[3] != tier` | tier differs from registry tier cell | Exact cell compare; all 213 cells are A/B/C. Enforced. |
| CAPTURE_PATH | regex, `islink`, `isfile`, realpath dir | not `corpus/captures/<24 hex>.txt`, or not a regular non-symlink file in LANE | Enforced; symlinked dir passes (R9). |
| CAPTURE_KEY | `sha256(url)[:24]` | key ≠ sha256(url)[:24] | Enforced. |
| CAPTURE_SHA | 16–64 hex + `…`/`...` prefix of sha256(capture) | shorter than 16 or not a prefix | Enforced; `...` accepted beyond spec (R3). |
| REFETCH (admit) | one row with id, url, key, fetched, curl 0, 2xx, txt_sha = capture sha | same | Enforced; reads the working-tree `refetch.tsv` (R5). |
| REFETCH (unreach) | row with id, url, fetched, curl_rc, http; or record is success (curl 0 and 2xx) | same | Enforced. "success" is inferred as curl 0 + 2xx (matches the admit definition); the docstring does not restate it. |
| WORDS | `len(quote.split())` | differs from whitespace-token count | Enforced. |
| QUOTE_LEN | `1 ≤ n ≤ 25` | <1 or >25 words | Enforced (rev 26 → QUOTE_LEN; 25 → OK). |
| QUOTE_ABSENT | normalized substring of normalized capture | does not occur | Enforced; substring, so quotes may cut words (documented as "exact"). Capture read with `errors="replace"` (not tested with an invalid-byte capture). |
| REV | 40-hex, `cat-file -t rev^{commit}`, `rev:path` is blob | not a commit in GITDIR, or path not a blob | Enforced. Refuses `..`, leading `/`, directories. Accepts `./` (R4). |
| LINE | `1 ≤ line ≤ len(blob)`, normalized quote in that line | outside blob, or quote not in that line | Enforced (line 1 vs 0 handled by parse). |

## Docstring / claims.md inconsistencies

1. Docstring: "reading only committed lane bytes". Code reads the working tree for SOURCES.md, captures and refetch.tsv (R5).
2. Docstring exit: "2 on … I/O error". Unreadable lesson/capture exits 1 with a traceback (F5).
3. Docstring rev form: `quote=<text to end of line>`; code refuses a leading `"` (F1). The docstring's own PARSE list does not mention it.
4. Docstring rev form: `path=<repo-relative path>`; code's space-split refuses spaced paths (F2).
5. Docstring url/admit template: `decision=<admit|reject>`; no check constrains it (R2). Unreach requires `reject` (consistent).
6. Docstring CAPTURE_SHA suffix `[…]`; code also takes `...` (R3).
7. Docstring REGISTRY: "Registry row"; code: any 11-cell row, any section (R8).
8. Docstring: "rev form … git objects in GITDIR (default LANE)"; GIT_DIR in the environment overrides `-C` (R7). Not documented.
9. claims.md K2 judges records against "committed" bytes; the tool judges working-tree bytes. Identical at the landing (`git diff` empty), so the frozen counter cannot distinguish them.
10. claims.md K3 names "meets every docstring check" as the harm test; F1 and F2 meet every documented check and still print FAIL, so the tool's undocumented refusals are themselves in K3 class.

## Verification gaps (not run)

- Quote-absent against an invalid-UTF-8 capture (only the refetch-side invalid bytes were run).
- A symlinked `corpus/captures` in a worktree (R9).
- `--repo` set to a subdirectory with a `./`-prefixed rev path (R4).
- Exhaustive key-order permutation fuzzing; only the frozen battery and the targeted matrix were run.
- Probes on the other claims predicates (C1 depth, round-83 lesson Gate block) — outside this seat.

## Pass bookkeeping

Pass 1 (`driver.py`) had three of my own fixture errors (quote starting `"` masked the path/line probes, a 23-token line labelled as 26, a broken mtime marker). Those receipts are kept under `superseded-pass1/` with a README, and are not cited as findings. Pass 2 (`driver2.py`) replaced them; its first run also had two fixture errors (`words=2` for a 3-token quote, `path=tools corpus` with a space), fixed before the receipts listed here were written.

## Tooling

No installs. Used existing `/usr/bin/python3` (3.14.8) and `/usr/bin/strace` (already present). No pacman, no `uv tool`, nothing written to `~/.local/bin` or any PATH directory.

## Recommended fixes (for the subject owner, not applied)

- Drop the rev-quote `"` rule (or document it); the form is unambiguous with `quote=` last.
- Parse rev `path=` by known keys rather than a space split, or document that spaced paths are unsupported.
- Either read committed bytes (`git show`) or document working-tree reading.
- Exit 2 on unreadable inputs, as documented.
- Constrain `decision` by form; accept only `…` in `capture_sha256`.
- Decide whether URL identity is part of the record's meaning; if so, add a URL-against-registry check (R1).

## Receipt index (`.ufo/waves/round-83/w1/R83ReviewerTool/`)

- Context: `g1-battery.txt` (frozen C2 counter on the landing tree: `GATE_RECORDS_R83=PASS`, rc 0), `g2-positives.txt` (15/15 OK, rc 0).
- F1: `k3a-rev-quote-leading-dquote.txt` (rc 1), `k3a2-rev-quote-docstring-line.txt` (rc 1).
- F2: `k3b-rev-path-with-space.txt` (rc 1).
- F3: `m-*.txt` (36 probes), `matrix-summary.txt`; pass-1 `w1–w12`, `x1–x11`, `c3-invalid-utf8.txt`.
- F4: `w1-admit-decision-reject.txt`, `w2-sha-ascii-ellipsis.txt`, `m-T-REV-dot-slash.txt`, `x-cross-url-same-id.txt`, `x-uncommitted-registry-row.txt` + `…-committed-check.txt`, `m-T-ZWSP-token-glue.txt`, `d-gitdir-env.txt`.
- F5: `x1–x11`, `c1-capture-unreadable.txt`, `c2-lesson-unreadable.txt`, `c3-invalid-utf8.txt`, `x-invalid-utf8-refetch.txt`, `x-formfeed-in-quote.txt`.
- F6: `d-strace-full.txt`, `d2-git-commands.txt`, `d-tree-diff.txt`, `d-strace-summary.txt`; `d3-no-network.txt` is a weak check (ran under `unshare -rn`, not proof of no network); the strace is the proof.
- Superseded (not cited): `superseded-pass1/`.

## Verdict by claim

Claim C2 — K2 held; K3 fired (F1, F2); K4 held (with the I/O exit-code deviation noted in F5). Purity held (F6).

VERDICT: R83ReviewerTool C2 fired — K3 fires: a genuine rev record quoting tools/gate-records.py line 85 (`quote=" ".join(s.split())`, which begins with a double quote) prints `FAIL PARSE` with exit 1 (`k3a-rev-quote-leading-dquote.txt`), and a genuine rev record for a committed path containing a space prints `FAIL PARSE` with exit 1 (`k3b-rev-path-with-space.txt`).
