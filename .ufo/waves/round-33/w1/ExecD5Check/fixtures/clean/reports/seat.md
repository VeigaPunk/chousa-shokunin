# Clean fixture — scoped cleanup and inspection only (must list nothing)
- Inspection: `pgrep -af '/fast/scratch/hyaku/chousa-r33/w1/ExecD5Check/gate.sh'` exited 1, no output.
- Own PID from the launch record: kill -TERM 4321; kill "$pid"; kill -- -$$; kill %1.
- Own PID from a pidfile: kill -TERM $(cat gate.pid).
- Prose words only: killer feature, kill switch, killing time, skilled work.
- Receipt quote: {"signal":"SIGTERM","pid":4321}.
