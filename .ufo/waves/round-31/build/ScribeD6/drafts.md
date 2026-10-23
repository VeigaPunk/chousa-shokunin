# D6 append-only correction drafts

## Target 1 — dead-seat record

**File:** `corpus/lessons/round-30.md`  
**Insertion point:** after line 150, in `## Seats and holds`, before `## Census` (line 152). Keep all preceding text unchanged.

```md
### 2026-10-23 correction to the dead-seat record (routed defect D6)

The preceding “Each is a hold, not retried” statement is not accurate for `CriticS047Live`: after its provider-quota HTTP 429 (“Individual quota reached”), the S047 real-page task was re-issued in the falsify wave as `LiveS047After` under the same `critic` role. Record this as a retry; this correction does not rewrite the earlier account. Evidence: `corpus/lessons/round-30-verifier-spotcheck.md:65-69`; `.ufo/waves/round-30/build-spec.json:147-150` and `falsify-spec.json:122-125`; `.ufo/waves/round-30/build-dispatch.json:323-332` and `falsify-dispatch.json:268-277`; `.ufo/waves/round-30/falsify/LiveS047After.md:4-10`.
```

## Target 2 — unreviewed refused-seat output

**File:** `.ufo/waves/round-30/falsify/ReviewQuality30.md`  
**Insertion point:** after line 44, still under `### 29`, before `## Residual risk and gaps` (line 46). Keep all preceding text unchanged.

```md
### 2026-10-23 correction to the criterion-29 control evidence (routed defect D6)

`CriticHarnessIntegrity` refused with `code=cyber_policy`; `.ufo/waves/round-30/controls/CriticHarnessIntegrity/leak-map.py` and `metadata-audit.py` are unreviewed output of that refused seat, not reviewed control evidence. Do not rely on the preceding characterization of `leak-map.py` as a keyed control or on the inference that these files may cover item-order or registry-id shortcuts; their coverage remains unverified. The earlier text is retained unchanged. Evidence: `corpus/lessons/round-30.md:143-146`; `timeout 30s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show --stat abfdf932` and `timeout 30s git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show --format= --name-only abfdf932` (both list the two scripts); the name-only output contains no seat report, and a current-path check found `.ufo/waves/round-30/build/CriticHarnessIntegrity.md` and `.ufo/waves/round-30/build/CriticHarnessIntegrity/` absent.
```

## Evidence and limits

The commit shown by `git show --stat` is `abfdf93274d0c70e02465e22abcf029dea59efb9`; its name-only listing contains exactly `.ufo/waves/round-30/controls/CriticHarnessIntegrity/leak-map.py` and `.ufo/waves/round-30/controls/CriticHarnessIntegrity/metadata-audit.py` for this seat. The report-presence check printed `ABSENT` for both the report file and directory. These are drafts only; no lesson or round-30 review text was changed.
