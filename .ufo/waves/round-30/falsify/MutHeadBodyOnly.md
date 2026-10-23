VERDICT: pass — KILLED; both mutant draws scored 88/106, below the target 106/106.
Axes: coverage and operability. Mutant narrows the head boundary to `</head>` or `<body>`, excluding other start tags and text; [diff](MutHeadBodyOnly/mutant.patch). Expected detector: the frozen C 1 counter.
Actual `QUOTE_REOPEN_HEADLESS_MATCH`: pristine 106/106 (exit 0); mutant draw 1 and draw 2 each 88/106 (exit 1); restored 106/106 (exit 0).
Per draw, misses: `headless-nobody/body-window` 10/10 and `headless-text/body-window` 8/8, all expected `VERBATIM`, got `ABSENT`; every other class/kind matched (88 items).
Evidence: [exact commands, outputs and exits](MutHeadBodyOnly/commands.txt); receipts [pristine](MutHeadBodyOnly/pristine.json), [draw 1](MutHeadBodyOnly/run1.json), [draw 2](MutHeadBodyOnly/run2.json), [restored](MutHeadBodyOnly/restored.json).
SHA-256 before and restored: `47a657e72f38f9424748a000b3bd218e26b6a601192b68e06a916471222a1201`; mutated: `6ed67447f2e52219c67693d5dece9f9964a7667eb5f049d8b22d2e38cf4624c6`. Scratch bytes restored exactly; production tool hash unchanged.
Frozen counter and harness hashes matched the supplied values before scoring and after restoration; receipts record their hashes. Each detector command had a 300 s timeout, 2 GiB address-space limit and 8192 process limit; all candidate processes exited without harness termination.
C 2 was not scored. No external fetches, installations or updates were performed; only the assigned scratch copy was mutated.
