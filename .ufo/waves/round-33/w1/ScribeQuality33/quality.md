## Round-33 additions (appended 2026-10-23; criteria 1–35 unchanged)

36. **Fixture metadata cannot stand in for semantics.** A coverage fixture assigns
    expected classes independently of directory enumeration, filename, creation
    order, mtime and inode; shuffle creation and randomize metadata order across
    classes. Before freezing the counter or admitting candidate data, score and
    commit separate metadata-order and no-source-reader control receipts with
    the frozen counter; each must show `matched < total`. Check: both controls'
    receipts are committed before freeze and each receipt's matched count is
    strictly below total. Shown able to fail: both metadata-control receipts
    report `matched=132`, `total=132`, `predicate_holds=true`
    (`.ufo/waves/round-32/w2/CriticAxis32/control-metadata-s32320021.json:12-15`,
    `control-metadata-s32320022.json:12-15`); that control picks the first 36
    paths sorted by mtime/inode (`.ufo/waves/round-32/w2/CriticAxis32/metadata-control.sh:30-37`)
    and opens zero citation sources (`.ufo/waves/round-32/w2/CriticAxis32/evidence-summary.json:20-26`). —
    `corpus/lessons/round-32-verifier-spotcheck.md:154-158,73-74`.

37. **Every numeric tally carries its counting command.** Each numeric tally in
    a report or SCORECARD states the exact command and scoped population used
    to derive it; rerunning that command must reproduce the stated number.
    Check: inventory the tally-bearing rows, require a command for each, and
    compare its output with the row. Shown able to fail: the report and
    SCORECARD state `10f2fe12 ×18`, while a census finds 20 committed receipt
    files on that gate, all 24/24; the extra two were excluded under an
    unstated convention (`corpus/lessons/round-32-verifier-spotcheck.md:159-162`). —
    `corpus/lessons/round-32-verifier-spotcheck.md:159-162`.

38. **A battery output begins with its revision header.** The first line of
    every battery output identifies both the lane revision and the gate
    SHA-256 against which the results were measured. Check: inspect the first
    line and fail if either value is absent. Shown able to fail:
    `measure/final/battery.out` has no `gate_sha256`/lane-revision header,
    whereas the base battery logs have one (`corpus/lessons/round-32-verifier-spotcheck.md:163-165`). —
    `corpus/lessons/round-32-verifier-spotcheck.md:163-165`.

39. **A seat signals only its recorded processes.** Before starting a
    background process, record its PID or process-group ID; every signal must
    target only that recorded PID/process group, never a process name or
    pattern. Check: audit each signal invocation against a prior matching
    PID/PGID record and reject name-based selectors such as `pkill` or
    `killall`. Shown able to fail: `RerunC1b` used `pkill -x sleep`, killing
    three sibling `sleep` processes (`corpus/lessons/round-32-verifier-spotcheck.md:145-146`);
    the routed repair requires signals scoped to the seat's own PID or process
    group (`corpus/lessons/round-32-verifier-spotcheck.md:168-169`). —
    `corpus/lessons/round-32-verifier-spotcheck.md:145-146,168-169`.
