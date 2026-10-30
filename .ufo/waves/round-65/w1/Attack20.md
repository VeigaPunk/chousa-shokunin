# Attack20 — C1 frozen case upper-digest attack (round65)

Seat: Attack20 (leaf attack seat, lane chousa round65). Freeze f99de3bdfaaf9b4c4fa85cc55dd37b9df2ee90fd. Base d6ed8155e9b4735639a2cf0a3e479c62f2056195. Scope: R65-C1 only; assigned frozen case `upper-digest`. No production writes; all probes bounded and isolated in scratch (deleted on exit). Tools installed: none (system python3 3.14.8 only; no uv/npx/pacman transactions needed).

## Axes named

1. **Digest-grammar strictness** — is the `[0-9a-f]{64}` hex grammar the actual boundary, or can a nearby digest mutation (near `upper-digest`) bypass the reference?
2. **Tokenization layer below the grammar** — the digest grammar operates on `str.splitlines()` output; what else does that line model accept?
3. **Counter detectability** — can the frozen 20-case counter see any of these bypass classes at all?

## Counterexample (constructed, outside the frozen 20)

Fifteen receipts were crafted against BASE `d6ed8155…:SKILL.md` (blob sha256 `4355e16a…ce1a`, confirmed locally by `git -C <lane> cat-file blob … | sha256sum`). All distinct from the frozen 20 and from sibling Attack15's crafted set where noted. Verdicts of the frozen reference validator `corpus/evidence/round65/controls/ref-receipt-pin.py`:

Accepted (rc=0), none in the frozen 20:
- `p12-vt-sep` — every LF replaced by vertical tab `\v` (**new class**)
- `p13-nel-sep` — every LF replaced by U+0085 NEL (**new class**)
- `p14-u2028-sep` — every LF replaced by U+2028 LINE SEPARATOR (**new class**)
- `p2-double-separator` — extra blank line between header block and body (independently confirms sibling Attack15 `leadblank.txt`)
- `p3-crlf` — CRLF line endings (independently confirms sibling Attack15 `crlf.txt`)

Rejected (rc=1), none in the frozen 20:
- `p1-mixed-digest` — partial-case digest (only every 3rd a–f letter uppercased; strictly between valid and the frozen full-upper case) → `FAIL digest header`
- `p4-exit-00` — `EXIT=00` leading zero → `FAIL header/body`
- `p5-dup-sha-line` — duplicate `SHA256=` header line before separator → `FAIL header/body`
- `p6-leading-blank` — blank line before `REVISION=` → `FAIL header/body`
- `p7-tab-after-digest` — tab instead of space before path → `FAIL digest header`
- `p8-space-only-body` — whitespace-only body → `FAIL header/body`
- `p9-ws-separator` — single-space separator line → `FAIL header/body`
- `p10-trailing-ws-path` — trailing space after path → `FAIL blob/digest`
- `p11-no-space-before-path` — no space between digest and path → `FAIL digest header`

Full transcript and receipts: `.ufo/waves/round-65/w1/Attack20/` (`report.md`, `probe-transcript.txt`, `evidence-receipts/`).

## Does the frozen counter detect it?

**No — structurally, for every out-of-set class.** `c1-count.py` builds exactly its 20 fixed receipts and presents only those to the tool. Nothing outside the enumeration is ever constructed or fed to a target, so a target that accepts `p2`/`p3`/`p12`/`p13`/`p14` still scores exactly `CASES=20/20 C1=PASS`. Detection of these classes is impossible for the frozen counter by construction, independent of target behavior.

**Digest grammar itself: airtight in this neighborhood.** The assigned frozen case `upper-digest` (full uppercase) is rejected; my strictly-nearer `p1` mixed-case mutation is also rejected by the same `re.fullmatch('[0-9a-f]{64}')`. No case-folding, prefix, spacing, or duplication variant of the digest line passes. The live bypasses sit one layer down, in the line tokenization (`splitlines()` accepts ~28 Unicode line boundaries; text-mode `read_text` erases CRLF; only `lines[3]` is checked so a doubled separator shifts the body window without tripping the separator check).

Baseline replication: frozen counter vs. the reference validator in this seat's scratch `--work` → `CASES=20/20 C1=PASS`, rc=0, work dir self-removed. Matches frozen `controls/c1-positive.txt`.

## Evidence

- `.ufo/waves/round-65/w1/Attack20/evidence-receipts/p0..p14` — fifteen crafted receipts (unique seat names).
- `.ufo/waves/round-65/w1/Attack20/probe-transcript.txt` — full reference-validator verdicts, one line per probe.
- Counter baseline replication run in scratch (transient `--work`, auto-removed; no log kept).
- No frozen bytes altered; reference validator invoked read-only. No network, no git/jj mutations; read-only `git -C` only.

## Impacted axes

R65-C1 predicate fidelity only. `C1=PASS` continues to mean "matches the frozen 20-case interface sample", not "receipt parser is safe". The claim text already narrows scope ("interface/consistency coverage, not … general parser safety"), which covers the accepted leniency classes. C1 numeric remains historical 3/10; no axis change.

## Smallest safe correction

None to frozen bytes — freeze/kill rule holds, the predicate is met by the reference, and the bypasses are inside the claim's declared scope boundary. For L1 integration only: (a) record that the reference validator accepts non-POSIX line structures (`\v`, U+0085, U+2028, CRLF, doubled separator) due to `splitlines()`/text-mode tokenization, and the frozen counter cannot see any of it; (b) if parser strictness is ever claimed in a future round, candidate cases: `p12`/`p13`/`p14` (Unicode boundaries), `p1` (mixed-case digest, for enumeration completeness). No counter edit, no case addition this round.

## Provenance honesty

- `p2`/`p3` independently reproduce sibling Attack15's `leadblank`/`crlf` accepted classes; attribution noted, no duplication claimed.
- Exit authenticity (a forged `EXIT=0` over failing output) and content forgery (digest over content never produced by the claimed tool) pass both validators by design — explicitly outside C1 ("not execution-authenticity claim"). A true digest forgery still requires a SHA-256 collision against a git blob; infeasible.
- `p1` is a coverage observation, not a live bypass: any implementation lenient enough to accept mixed-case hex would accept full-upper hex and fail the frozen `upper-digest` case transitively.
