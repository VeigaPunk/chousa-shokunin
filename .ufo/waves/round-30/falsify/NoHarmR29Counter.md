VERDICT: holds — landed tool keeps the round-29 claim (QUOTE_REOPEN_MATCH=130/130, exit 0); research-gate.sh unchanged; round-1 count 3/3.

Target: no harm to the round-29 claim from the round-30 landed `tools/quote-reopen.py`.

Lane HEAD `a9d3a05a8fd812a60323b08381019152069581fd`; `sha256sum tools/quote-reopen.py` =
`47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201` (matches the landed hash).

1. Round-29 counter, run once on the landed tool (counter SHA-256 `cd509650…5c175d`):
   `timeout 600 python3 corpus/evidence/round29/c1-count.py --receipt .ufo/waves/round-30/falsify/NoHarmR29Counter/receipt-r29-c1.json -- python3 tools/quote-reopen.py verify`
   (under `ulimit -v 4000000`). Output: `QUOTE_REOPEN_MATCH=130/130`, exit 0,
   `seed=10740203419086734782 tool_exit=1 wall_s=2.31`, `predicate_holds: true`. Every class is full:
   runtime-page-window 24/24, runtime-page-transpose 24/24, runtime-subspan / transpose / crossattr 14/14 each,
   verbatim-inline-markup 9/9, the 5 absent classes 4/4 each, too-long-true-text 3/3, no-source 2/2 and 1/1.
   No non-matching items. The counter GETs the registry URLs of S002 S003 S008 S013 S019 S020 S038 S044 itself
   (URLs read from `corpus/SOURCES.md` rows, `registry_url`, line 115); the receipt is the record of that fetch.
   Note: an earlier attempt that same session exited 1 before scoring. My own `ulimit -u 512` cap is per user,
   and the host already runs more processes than that, so the fork raised `BlockingIOError: [Errno 11]` at line 266.
   That attempt was a failed measurement and is not scored. The rerun above had no process cap.
   Its receipt replaces the failed one at the same path.
2. `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin diff --quiet a3a3710e a9d3a05a8fd812a60323b08381019152069581fd -- tools/research-gate.sh`
   exited 0 (no change). Current `tools/research-gate.sh` SHA-256 is `ac1315dd…835765`.
3. Round-1 counting command, copied exactly from SCORECARD.md lines 28-30 and run from the lane root under `timeout 600`:
   output `VERDICT_BEARING_EXPORTS=3/3`, exit 0 (expected 3/3).

Residual risk: 1 round-29 run, as assigned. It does not cover page-content drift between fresh seeds.
Tools installed or updated: none.
