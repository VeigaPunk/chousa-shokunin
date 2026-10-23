# SentinelC2After
Verdict: HOLDS for tested scope; severity: none.
Attack/repro: on scratch gate SHA-256 `10f2fe12043c6f1565c7d7b9446ee0c4dc11e9649aa3350dcab96f8a2ccb4098`, ran `timeout 120s strace -f -e trace=%file,%network … verify-chain {unresolved,resolved}.md --root corpus` (both exit 1); outputs: `/fast/scratch/hyaku/chousa-r32/w2/SentinelC2After/unresolved.out:2-20` and `resolved.out:2-22`.
Evidence: U rows read only in-root target/internal symlink/`../`-within-lane/absolute-in-root (h1,h2,h4,h6 resolvable); matched resolved controls verified. Out-root symlink, `../../` escape, `/etc/passwd`, 8,388,609-byte file (cap 8,388,608), character device, and HTTPS URL stayed exempt on U; resolved controls refused them as out-of-corpus, read-too-large, non-regular, or external.
Network: `grep` for `socket|connect|sendto|sendmsg|recvfrom|recvmsg` in both strace logs returned no matches; `https://127.0.0.1:9/no` was external/refused, not fetched.
Code evidence: U and resolved arms both call `chain_probe` (`tools/research-gate.sh:1904-1908,1944-1955`); it uses shared canonicalization/boundary/regular-file/size checks (`1213-1297`) and local `cat` only (`1841-1849`).
Impact/remediation: no C2-specific boundary or network path found; no remediation needed. Limits: static-path tests only (no concurrent stat→read race test); C1/C2 counters not run; no tools installed.
