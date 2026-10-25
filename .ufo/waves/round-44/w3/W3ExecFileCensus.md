# W3 — sources-census validate-before-append mirror (round-44 corpus)

Seat: leaf, wave 3, round 44. Read-only on production; probes used `/tmp` only.
Script under test: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` (SOURCES-CONTRACT-v1 validator).

## 1. Command as run

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate \
  --file /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/validate/corpus/SOURCES.md
```

## 2. Verbatim stdout and exit code (executed 2026-10-24)

```
file	W04	S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
file	W04	S053 duplicate url docs.python.org/3/library/socket.html across scopes
file	W04	S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	W04	S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
file	W04	S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
file	ok	/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/assimilation/validate/corpus/SOURCES.md
EXIT_CODE:0
```

(Lane label is the literal `file` — `--file` mode names its single target that way.)

## 3. E03 / E04 verdict

**No E03 (duplicate id) and no E04 (duplicate URL within scope, non-rejected, no supersedes) finding appears.** The only findings are five W04 warnings ("same URL across scopes"), which per the script contract "do not affect clean lanes", hence exit 0 (`0` = clean or warnings). The mirror passes: the landed round-44 corpus state is clean for appending.

## 4. Why the mirror result is trusted (not vacuous) — probes run this session

| Probe | Command shape | Result |
|---|---|---|
| Negative control (live-fire) | `/tmp/w3-census-probe/SOURCES.md` with a duplicated id `S901` and a same-scope repeated URL `x.example/c` (S902→S903), validated with the same `--file` mode | Printed `file	E03	S901 duplicate id` and `file	E04	S903 duplicate url x.example/c within scope s3`; `NEGCTRL_EXIT:1`. E03/E04 detection works on this build. |
| Selftest | `sources-census.sh selftest` | `selftest ok`, exit 0 (all mutant checks `killed`, incl. `E03-duplicate-id`, `E04-duplicate-url`, `H1-no-table-cell-execution`). |
| Independent id recount | awk over the corpus table's id cells | 81 registry data rows (S001–S081), `uniq -d` → empty. |
| Independent used-by check | every `corpus/….md` referenced in the file tested against the validate corpus root | none missing — E11 was actually exercised (its root resolves to `…/round-44/assimilation/validate/`), not skipped. |

## 5. Account of the five W04s (all expected, none new)

The normalizer strips `#fragment` and trailing `/` and lowercases the host, so these pairs collapse to one URL across different scope cells; the first occurrence per URL is silent:

- **S051** after S050 — one HTML 5.2 page (`…/syntax.html`), two anchor scopes; the search log itself records this as a known W04 pair.
- **S053** after S052 — one `socket.html` page, two sections/scopes.
- **S074** after S059 — `hashlib.html`; S074 is additionally `status=rejected`, so it is doubly safe.
- **S073** and **S075** after S071 — the canonical `coreutils.html` printed in the roff tty-links of the sha256sum/env/mktemp rows; S070 (sha256sum, local path only, no URL) is outside URL tracking entirely.
- All same-scope URL repeats in this file (S029–S033) carry `supersedes S0NN` in `teaches`, which is exactly the E04 exemption — so E04 stays silent legitimately.

## 6. Calibration notes — latent quirks observed, none triggered today

1. **Backtick-adjacent URL capture.** `url_of` matches `https?://[^[:space:]|]+`, so S067's backtick-wrapped URL normalizes with a trailing backtick (`man7.org/.../execvp.3.html\``). A future row citing the same page un-backticked would evade both E04 and W04 via a different key. Only one man7.org row exists, so no finding today; this is a dedupe-evasion vector for the validator's next mutation round.
2. **Supersedes exemption is textual.** E04 exempts any row whose `teaches` matches `supersedes S[0-9]{3}`, regardless of whether a real supersede relation exists. All five current users (S029–S033) name real predecessors, so the landed state is sound, but the exemption is spoofable by a single substring.
3. **Blank-line table gap.** Blank lines before S079–S081 (lines 89, 93 of the corpus file) would split the table for a strict Markdown renderer, but the parser resets only on headings, so all 81 rows count as Registry rows. Census membership and rendered view can drift apart by construction; membership is unaffected here.

## 7. Scope

No production file, lane index, jj state, fleet repo, sibling repo, or `/home/vgpnk/Projects/shokuknow` was modified. No network, no fetch, no subagent dispatch. Probes wrote only under `/tmp/w3-census-probe/`. This report is the single file written.
