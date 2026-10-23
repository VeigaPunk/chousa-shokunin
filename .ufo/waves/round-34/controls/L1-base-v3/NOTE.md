# Do-nothing control under counter v3 (L1)

Base gate `43a1af35…4346`, counter v3 `970cf9a7…da2a`.
- seeds 3491, 3492, default host locale (en_US.UTF-8): gate run exceeded the counter's 1500 s bound
  (`gate_timed_out=true`), every record scores `none`: `LONGSPAN_MATCH=0/42`.
- seed 3493 with `LC_ALL=C` in the counter's environment: `LONGSPAN_MATCH=25/42` (every long
  supported/mislocated class misses; all short and long-unsupported classes match).
ExecPerfProfile measured the base's per-byte `json_unescape` 3.3x slower under UTF-8; the L1 runs the
control re-scores and every candidate measurement with `LC_ALL=C` and records that in this note.
