# Round 36 C1 S12 — C-locale UTF-8 decode

**Verdict: R4/S12 reproduced.** At lane tip `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`, the landed gate decodes `\u00e9` to UTF-8 `é` and matches the fixture under `LC_ALL=C`; the byte-exact round-35 base control leaves the escape undecoded and reports the span unsupported. Unsetting the locale variables for the landed gate did not change the result.

The assigned axis is **C1 operability, scenario S12 (C-locale decode)**; this scoped experiment does not score C1's 14-scenario predicate or C2.

## Source and pinned gate identity

`tools/research-gate.sh:1442-1507` defines `json_unescape`. It sets and exports local `LC_ALL=C` (1457-1458), parses `\uXXXX`, and encodes code points below U+0800 as two octal-escaped bytes (1490-1494); U+00E9 therefore becomes `C3 A9`. The landed path's decisive source lines are 1457-1494. The base control's `json_unescape` is at `.ufo/waves/round-36/controls/base-gate-r36.sh:1419-1470`; it uses `printf -v c '%b' "\u$hex"` at 1457-1459 without pinning `LC_ALL`, which under the tested C locale preserves the escape rather than producing `é`.

Located quote (accessed 2026-10-23): “decoder therefore encodes UTF-8 by hand and runs in the same byte scope the span matchers carry.” — `tools/research-gate.sh:1455-1458`.

Pinned identities read on 2026-10-23:

- `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master` → `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`.
- Landed `tools/research-gate.sh` SHA-256: `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`.
- Base `.ufo/waves/round-36/controls/base-gate-r36.sh` SHA-256: `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`.

## Fixture and deciding output

The scratch source is one line, `café` plus LF. The JSONL span is escaped as `caf\u00e9`; the visible-output variant also escapes the ID as `C-\u00e9` so the gate's own claim output displays the decoded character.

With `LC_ALL=C`, landed output (exit 0):

```text
CLAIM id=C-é expected=supported observed=supported source=source.md at=line:1 verdict=match
RESEARCH_GATE: CLEAN (claims=1 supported=1 contradicted=0 unsupported=0 mismatched=0 unproven=0 refused=0 invalid=0 findings=0 drift=0)
```

With `LC_ALL=C`, base-control failure (exit 1):

```text
CLAIM id=C-\u00E9 expected=supported observed=unsupported source=source.md at=- verdict=mismatch
FINDING CLAIM_SPAN_NOT_FOUND severity=warn surface=claims obs=id=C-\u00E9 nearest_line=- context=-
RESEARCH_GATE: DRIFT (claims=1 supported=0 contradicted=0 unsupported=1 mismatched=1 unproven=0 refused=0 invalid=0 findings=1 drift=1)
```

The extra landed run with `LC_ALL`, `LC_CTYPE`, and `LANG` unset also exited 0 and printed `CLAIM id=C-é ... observed=supported ... verdict=match`: unsetting them changed nothing. The byte proof `LC_ALL=C printf 'é' | od -An -tx1` produced `c3 a9` (exit 0).

## Commands run (verbatim), status, and decisive evidence

All timeout bounds were within the brief. Commands 1–10 below are the complete shell-command list for this scoped experiment; status and the deciding output are recorded for each.

1. Exit 0; revision and both gate pins:

```sh
timeout 30s bash -lc 'git -C /home/vgpnk/Projects/shokunin/chousa-shokunin rev-parse master && sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh'
```

Output deciding identity: `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`; landed hash `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; base hash `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`.

2. Exit 0; created the assigned receipt directory and initial scratch source/JSONL (no stdout; source `café`, claim span `caf\u00e9`):

```sh
timeout 30s bash -lc 'mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecLocaleDecode /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture && printf "%s\n" "café" > /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/source.md && printf "%s\n" '\''{"id":"C-UTF8","source":"source.md","span":"caf\u00e9","expect":"supported"}'\'' > /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims.jsonl'
```

3. Exit 0; landed C-locale run on the initial fixture; deciding line:
`CLAIM id=C-UTF8 expected=supported observed=supported source=source.md at=line:1 verdict=match`.

```sh
timeout 900s env LC_ALL=C bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture
```

4. Exit 1; base C-locale run on the initial fixture; deciding lines:
`CLAIM id=C-UTF8 expected=supported observed=unsupported source=source.md at=- verdict=mismatch` and `FINDING CLAIM_SPAN_NOT_FOUND ...`.

```sh
timeout 900s env LC_ALL=C bash /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh verify-claims /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture
```

5. Exit 0; landed run with locale variables unset on the initial fixture; deciding line:
`CLAIM id=C-UTF8 expected=supported observed=supported source=source.md at=line:1 verdict=match`.

```sh
timeout 900s env -u LC_ALL -u LC_CTYPE -u LANG bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture
```

6. Exit 0; UTF-8 byte proof; output ` c3 a9`:

```sh
timeout 10s bash -o pipefail -c "LC_ALL=C printf 'é' | od -An -tx1"
```

7. Exit 0; created visible-output JSONL (no stdout); its line is `{"id":"C-\u00e9","source":"source.md","span":"caf\u00e9","expect":"supported"}`:

```sh
timeout 30s bash -lc 'printf "%s\n" '\''{"id":"C-\u00e9","source":"source.md","span":"caf\u00e9","expect":"supported"}'\'' > /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims-visible.jsonl'
```

8. Exit 0; landed C-locale visible-output run; deciding line:
`CLAIM id=C-é expected=supported observed=supported source=source.md at=line:1 verdict=match`.

```sh
timeout 900s env LC_ALL=C bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims-visible.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture
```

9. Exit 1; base C-locale visible-output run; deciding lines:
`CLAIM id=C-\u00E9 expected=supported observed=unsupported source=source.md at=- verdict=mismatch` and `FINDING CLAIM_SPAN_NOT_FOUND ...`.

```sh
timeout 900s env LC_ALL=C bash /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh verify-claims /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims-visible.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture
```

10. Exit 0; landed visible-output run with locale variables unset; deciding line:
`CLAIM id=C-é expected=supported observed=supported source=source.md at=line:1 verdict=match`.

```sh
timeout 900s env -u LC_ALL -u LC_CTYPE -u LANG bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-claims /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims-visible.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture
```

11. Exit 0; receipt hash:

```sh
timeout 10s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecLocaleDecode/locale-r4-receipt.txt
```

Output: `8635c3bcbc1613419c209906a9b4a49b71368d3ed9ef6f14b0792f62b2bfc6e8  /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecLocaleDecode/locale-r4-receipt.txt`.

## Files accessed (all 2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecLocaleDecode.md`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`.
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh` (search result and lines 1441-1561).
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh` (search result and lines 1418-1561).
- `/tmp/hyaku/chousa-r36/w1/ExecLocaleDecode/fixture/claims.jsonl`, `source.md`, and `claims-visible.jsonl`.

## Changed files, artifact, and scope

- Wrote this report once: `.ufo/waves/round-36/w1/ExecLocaleDecode.md`.
- Wrote receipt only under the assigned artifact directory: `.ufo/waves/round-36/w1/ExecLocaleDecode/locale-r4-receipt.txt` — SHA-256 `8635c3bcbc1613419c209906a9b4a49b71368d3ed9ef6f14b0792f62b2bfc6e8` (2611 bytes).
- No lane production file changed; no packages installed; no other axis or full counter was run. No blocker observed.
