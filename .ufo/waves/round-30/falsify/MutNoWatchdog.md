VERDICT: pass — KILLED: removing the watchdog scores 25/27 twice; pristine and restored score 27/27.
Axes: coverage, operability. Mutation removes only timer construction, daemon assignment and start; patch: `MutNoWatchdog/mutant.patch`.
Expected detector: frozen C 2 requires `QUOTE_REOPEN_FETCH_BOUND_MATCH=27/27`; full bounded commands, exit codes and hashes: `MutNoWatchdog/evidence.json`.
Receipts under `MutNoWatchdog/`: `pristine.json` and `restored.json` print 27/27 (exit 0); `run1.json` and `run2.json` print 25/27 (exit 1 each).
Each mutant run misses only drip-head: 2/2 have no verdict and are killed at 20.021–20.027 s, beyond bounds of 5.44–7.34 s; the other 25 items match, with no unrouted destinations.
SHA-256 before/restored/production: `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`; mutant: `9f370dd62e37b60a1c81732b58ca0c7e77e487d63c32f1c9582a5721fff8322f`; byte comparison exits 0; frozen hashes match.
Initial 2 GiB baseline scored 20/27 (exit 1), with MemoryError and thread-start errors: inconclusive, preserved as `MutNoWatchdog/pristine-limit.json`; all scored phases use an 8 GiB address-space cap and process cap 4096.
Exact scratch bytes restored; no matching candidate processes remain. No external fetch, production edit, or tool installation.
