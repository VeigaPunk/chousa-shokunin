# Probe10 — round65 word-exit probe findings

**Verdict: reference `controls/ref-receipt-pin.py` agrees with the independently derived oracle on all 35 EXIT-word cases (35/35 AGREE, 0 mismatches).**

- Scope: one surface only — the receipt header's `EXIT=` word. No battery, no production writes.
- Frozen format basis (claims.md C1): `EXIT` is decimal 0..255; exits 0 consistent / 1 invalid / 2 usage-environment.
- Independent oracle: accept iff the word is a canonical ASCII decimal numeral in [0,255] (no leading zeros except bare `0`, ≤3 digits, value ≤255).
- Fixture: isolated scratch git repo (`git init`, no clone); blob `pin.txt` at `070c12f9d4f6204b4543b1141024214f2f57b262`, digest `82823303…39131519`; REVISION and SHA256 headers held valid in every case so only the EXIT word varied. argv/output preserved.
- Accepted (exit 0, `RECEIPT_PIN=PASS`): `0 1 9 42 127 200 255`.
- Rejected (exit 1, `RECEIPT_PIN=FAIL header/body`): leading zeros (`00 01 09 042 0255 000`); out of range (`256 257 300 999`); overlong (`1000 10000`); empty/signed/whitespace (`"" -1 +1 " 42" "42 " \t42 42\t "4 2"`); non-decimal notation (`0x2a 0b101010 2.5 2a 4_2`); Unicode digit lookalikes (Arabic-Indic `٤٢`, fullwidth `４２`, `4²`).
- Exit 2 never observed for word-level malformations; they consistently map to exit 1, matching the frozen 0/1/2 contract.
- Boundaries 255/256 and 999/1000 are sharp; no edge case diverged from the frozen wording.

Evidence (`.ufo/waves/round-65/w1/Probe10/`): `probe10-word-exit-matrix.tsv` (full matrix), `probe10-receipt-w00/w11/w13/w32.txt` (exemplars), `probe10-word-exit-probe.py` (driver), `probe10-fixture-meta.env` (versions, fixture rev/digest).

Environment: python3 3.14.8, git 2.56.0 (preinstalled; no installs/upgrades). Pacman untouched; no network; read-only git on sources; scratch `/fast/scratch/hyaku/chousa-r65/Probe10/` deleted after evidence copy.

Risks: single-surface probe by assignment; production `tools/receipt-pin.py` not yet exercised (does not exist); L1 owns integration verification.
