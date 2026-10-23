# Prose fixture — citations of the D5 rule (all fail-closed as hits)
Seats MUST NOT run `pkill -x sleep` on the shared host (routed defect D5).
Ban list quoted verbatim: pkill, killall, kill $(pgrep ...), and pgrep | xargs kill.
A deny-list table row: | pkill | forbidden | by name only |
Permitted and not a hit: kill "$pid", kill -- -$$, and pgrep -af gate.sh.
