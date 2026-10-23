# Round 36 W1 — ExecHashShim (C1 S11)

**Axes:** C1 operability, S11 manifest-hash identity. C2 calibration was outside this scoped move and was not exercised.

## Verdict

**S11 PASS on the landed gate; base-control arm fails. The brief's requested landed-gate refusal did not occur.** With the hostile `sha256sum` first on `PATH`, landed `verify-all --json` exited 0, reported CLEAN, and wrote true 64-hex identities. The base control also exited 0/CLEAN but wrote the attacker's all-zero digest into both identity fields. Thus this run supports S11's stated pass condition and reproduces the control failure; it is not a full C1 counter run.

The requested “landed gate's refusal” / unchanged-manifest check is not applicable to this hostile-PATH run: the landed gate did not refuse and each fresh manifest contains one JSONL line. In source, hash failure is explicitly named as `research-gate: sha256sum unavailable or returned a non-hex value; manifest not written` (11-word located quote; `tools/research-gate.sh:3708-3709`, accessed 2026-10-23), followed by exit 2 before manifest-line construction and append (`:3703-3710`, `:3726-3728`, `:3787-3789`). This refusal path was not triggered or experimentally verified here. The landed helper uses `/usr/bin/sha256sum` (fallback `/bin/sha256sum`) and requires 64 lowercase hex (`:432-442`); the hostile PATH shim therefore did not control its hash result.

## Pinning and fixture

`git rev-parse master` returned `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`. The scored landed gate SHA-256 was `a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; the base control was `a47688518e509edbf43b433a5e16e1cf2481233f3acedb5824ba341f7f0c38ad`.

I used the S11 fixture shape in `corpus/evidence/round36/c1-count.py:150-197`: record, claims, and primary source under `/tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/`. The first PATH entry was `/tmp/hyaku/chousa-r36/w1/ExecHashShim/hashbin`, containing an executable `sha256sum` that prints the fixed all-zero 64-hex digest and exits 0. Clean PATH suffix: `/usr/local/bin:/usr/bin:/bin`. Each gate received the same fixture with a distinct new manifest pathname. The true record hash was `721d2837dfeeba3a88405a42053c818ae7233ae5e8b1b452d27ac0f00b854fde`.

## Runs and deciding output

Both commands were bounded by `timeout 180s`; the printed `EXIT=0` is the gate return code captured by the wrapper. The displayed gate output was identical in both runs:

```text
research-gate v2 — ts=2026-10-23T21:26:02Z — mode=verify-all — record=/tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/record.md — claims=/tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/claims.jsonl — root=/tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d
SECTION structure state=run verdict=CLEAN findings=0 drift=0
SECTION claims state=run verdict=CLEAN findings=0 drift=0 tally=VERDICT_BEARING_CLAIMS=1/1
SECTION chain state=run verdict=CLEAN findings=0 drift=0 tally=RESOLVED_HOPS=1/1
SECTION sweeps state=run verdict=CLEAN findings=0 drift=0 tally=VERIFIED_SWEEPS=1/1 REJECTIONS_OK=1/1
SECTION integrity state=run verdict=CLEAN findings=0 drift=0 tally=INTEGRITY refs=3 resolved=3 unresolved=0
VERIFY_ALL sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0
RESEARCH_GATE: CLEAN (sections=5 run=5 absent=0 drift-sections=0 findings=0 drift=0)
EXIT=0
```

Commands, verbatim as invoked, with exit codes and answer-bearing lines:

1. `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh` — exit 0. Output pinned the landed and base hashes above.
2. `timeout 30s git rev-parse master` — exit 0; output was `700bd5fcbf9abc118a6a0f078d51a2e7460c2878`.
3. `timeout 30s mkdir -p /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/lib /tmp/hyaku/chousa-r36/w1/ExecHashShim/hashbin /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim` — exit 0; no output.
4. `timeout 180s env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE PATH=/tmp/hyaku/chousa-r36/w1/ExecHashShim/hashbin:/usr/local/bin:/usr/bin:/bin bash /home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh verify-all /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/record.md --claims /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/claims.jsonl --json /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/manifest-landed.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d; rc=$?; printf 'EXIT=%d\\n' "$rc"` — gate exit 0. Deciding output: `RESEARCH_GATE: CLEAN ...` and `EXIT=0`; manifest fields below are both true hashes.
5. `timeout 180s env -u CHOUSA_RECORD -u CHOUSA_CLAIMS -u CHOUSA_AGGREGATOR_ERE PATH=/tmp/hyaku/chousa-r36/w1/ExecHashShim/hashbin:/usr/local/bin:/usr/bin:/bin bash /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh verify-all /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/record.md --claims /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/claims.jsonl --json /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/manifest-base.jsonl --root /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d; rc=$?; printf 'EXIT=%d\\n' "$rc"` — gate exit 0. Deciding output: `RESEARCH_GATE: CLEAN ...` and `EXIT=0`, despite both manifest identity fields being poisoned.
6. `timeout 30s cp /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/manifest-landed.jsonl /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/landed-manifest.jsonl && timeout 30s cp /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/manifest-base.jsonl /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/base-manifest.jsonl` — exit 0; no output.
7. `timeout 30s sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/landed-manifest.jsonl /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/base-manifest.jsonl /tmp/hyaku/chousa-r36/w1/ExecHashShim/hashbin/sha256sum /tmp/hyaku/chousa-r36/w1/ExecHashShim/fx-d/record.md` — exit 0; hashes are listed below.
8. `timeout 30s wc -l /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/landed-manifest.jsonl /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/base-manifest.jsonl` — exit 0; each manifest had one line (`1`, `1`, total `2`).

The deciding manifest values:

- Landed: `record_sha256=721d2837dfeeba3a88405a42053c818ae7233ae5e8b1b452d27ac0f00b854fde`, `gate_sha256=a7d3922c768a217a2dcedf347b4de438b8dda4108e1335f5a39af6117e1f54e8`; neither is poisoned.
- Base: `record_sha256=0000000000000000000000000000000000000000000000000000000000000000`, `gate_sha256=0000000000000000000000000000000000000000000000000000000000000000`; both are poisoned. The base still reports CLEAN and returns 0.

## Retained artifacts

All retained receipts are below `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1/ExecHashShim/` and are under 1 MiB:

- `landed-manifest.jsonl` — SHA-256 `5108b44655d31cf6c56cc6aeee8dfc55afcd16cd905ba546db880d2416984781`.
- `base-manifest.jsonl` — SHA-256 `a4ce5a4d784d61b65b5f4cb6845a33fa4f478de47231ed767b946c966e0a42f8`.

Hostile shim used: `/tmp/hyaku/chousa-r36/w1/ExecHashShim/hashbin/sha256sum`, SHA-256 `f1824d1c768252a7504a89eef096dda29424b4852d8870290ee8e224d371691b`.

## Files opened or hashed (access date 2026-10-23)

- `/home/vgpnk/.agents/skills/godspeed/SKILL.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/w1-briefs/ExecHashShim.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/claims.md`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c1-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round36/c2-count.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/argv-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/mechanism-witness.py`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/tools/research-gate.sh`
- `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-36/controls/base-gate-r36.sh` (hashed; not content-read)
- Scratch fixture and manifest files under `/tmp/hyaku/chousa-r36/w1/ExecHashShim/` (created/accessed during these runs)
- The two retained manifest artifacts above.

The `measure/` and `controls/` directories were listed; no committed receipts were altered. No tools were installed. No build, lint, tests, or formatters were run.