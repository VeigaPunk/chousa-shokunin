# FxMetaHeading — verify-metadata boundary review

Axis: operability. No production files changed.

Checkpoint used: private clone HEAD `e93ac711f885a10d44fdd80a1734997419595b5a` (observed with `git rev-parse HEAD`). The initially assigned `0fc037e` is not the tested gate: `corpus/lessons/round-25.md:111-125` records it omitted `tools/research-gate.sh` (prose claimed 154 cases; gate SHA `752e4e38…`, 136 cases). `d8c8cff` fixed the gate but still omitted `corpus/evidence/README.md` (`round-25.md:127-133`). I used the corrected full checkpoint, not either incomplete package.

LSP: `read xd://lsp` returned `No such tool`; the mounted-device list had no LSP. I used literal source reads and runtime probes; grep only located candidate lines and is not semantic proof.

## Finding — P3 contract ambiguity, not a confirmed implementation defect

Spec v1 says the header ends before the first `## ` heading outside a fence, or is the whole file when none (`corpus/evidence/round25-claims.md:24-25`). The post-registration entry repeats that boundary (`corpus/knowledge/metadata-screen-r25.md:31-35`). The implementation is explicitly lexical: after fence handling it breaks on `^##[[:space:]]+` (`tools/research-gate.sh:2349-2375`); it does not parse Markdown comments. No semantic Markdown claim or comment rule is stated in v1, so the comment result below is an implementation choice, not evidence of semantic misparsing.

Exact per-case commands, rc, complete stdout/stderr, and fixtures are saved in `/tmp/chousa-r25-FxMetaHeading/metadata-heading-probe/heading-boundary-probe.log` (inputs beside it). Command form was `(cd /tmp/chousa-r25-FxMetaHeading && bash tools/research-gate.sh verify-metadata /tmp/chousa-r25-FxMetaHeading/metadata-heading-probe/<case>.md --root /tmp/chousa-r25-FxMetaHeading)`.

- `real-h2.md` (`## Actual heading`): rc 1; `recheck=absent`, `META_RECHECK_ABSENT`. **Specified; match.**
- `fenced-h2.md` (`## Fenced text` between triple-backtick fences): rc 0; `recheck=scheduled`, CLEAN. **Specified; match.**
- `tab-after-hashes.md` (`##\tTabbed separator`): rc 1; `recheck=absent`, `META_RECHECK_ABSENT`. **Ambiguous:** v1 writes the literal `## ` but does not define separator grammar. The implementation accepts a tab via `[[:space:]]+`; under a strict ASCII-space reading this is a divergence, but v1 does not explicitly reject tabs.
- `h3.md` (`### Third level`): rc 0; scheduled/CLEAN. **Specified by the `## ` marker; match** (three hashes do not match the H2 prefix).
- `html-comment.md` (`## Commented line` between `<!--` and `-->`): rc 1; `recheck=absent`, `META_RECHECK_ABSENT`. **Unspecified; implementation choice.** I make no claim whether this is a semantic Markdown heading.
- `h1-only.md` (`# Title`): rc 0; scheduled/CLEAN. **Specified by the `## ` marker; match.**
- `no-h2.md`: rc 0; scheduled/CLEAN. **Specified whole-file fallback; match.**

The post-registration refusal path is documented at `metadata-screen-r25.md:41-46` and implemented before parsing at `research-gate.sh:2324-2342` (denylist/canonical path, 8 MiB cap, NUL refusal, counted as drift). These ordinary fixtures did not exercise those refusal branches; they do not affect the boundary observations above.

## Residual risk / verification gaps

The accepted tab separator and HTML-comment behavior are not fully specified; tighten v1 only if the lane needs exact choices. No full selftest or separate hardening-branch suite was run (outside this heading-boundary assignment). No tool installed or updated.

Probe artifacts written in private clone (SHA-256):
- `metadata-heading-probe/fenced-h2.md` — `78d0c57604ed55b60fbcc524a98a730c3b434995c62109095d9ff78c1cd39947`
- `metadata-heading-probe/h1-only.md` — `3c20773331b089582529718ba70434a95c71725f20e4da858fc59eeb4c71a283`
- `metadata-heading-probe/h3.md` — `a0b2b53d2fda2f581094b914f28a2f11c14282c1440d7b86b0b802d0afd5749a`
- `metadata-heading-probe/html-comment.md` — `699258d8dd546b2cba8cda8d7ceecdd75b8400938b3b4e170d950a59db87afe7`
- `metadata-heading-probe/no-h2.md` — `9437ef69d4d24dd7cbc6605c849502345e4285a4569e63b24383168e0bc4a4c4`
- `metadata-heading-probe/real-h2.md` — `c073a534316fbebf7584ad0a2344a90469963060a88e64d85e68861345320cbe`
- `metadata-heading-probe/tab-after-hashes.md` — `83c152d0b2a830af50a48b2cf81c160e7b12ec624e15057a1d9e0bf6dbe65233`
- `metadata-heading-probe/heading-boundary-probe.log` — `d2b6310b4ea14173ca05b682e2cf740dbd8b0a6e73296e6c701ead1d1b25384d`

VERDICT: The tested real/fenced/H3/H1/no-H2 cases match v1; tab and comment behavior remain under-specified, with no confirmed actionable code defect.