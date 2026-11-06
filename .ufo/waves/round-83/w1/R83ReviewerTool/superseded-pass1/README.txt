Superseded pass-1 receipts (kept for transparency; NOT cited as findings).
w4-key-order-shuffled: fixture error (quote= placed mid-line, which the docstring forbids); superseded by pass-2 matrix.
w8-rev-path-leading-slash, w9-rev-path-dotdot, w15-rev-line-0: fixture error (quote began with a double quote -> PARSE, the K3 cause, masked the path/line probe); re-run in pass 2 with a valid quote (T-REV-leading-slash, T-REV-dotdot, T-REV-line-leading-zero).
w14-rev-26-words: fixture error (line sliced to 23 tokens; the WORDS result was correct); re-run in pass 2 (T-QLEN-26-rev, T-QLEN-25-rev-boundary).
d1-no-writes-INVALID-marker.txt: marker set with utime(0,0), so find -newer listed the whole tree; invalid. Replaced by tree-vs-fresh-archive diff (d-tree-diff.txt) and strace (d-strace-full.txt).
