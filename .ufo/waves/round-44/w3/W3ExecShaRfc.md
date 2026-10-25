# W3ExecShaRfc — round-44 wave 3 leaf report

Seat: leaf (no subagent dispatch). Date: 2026-10-24.
Scope: falsify/check the claim that RFC capture file name `d0c4a09a9de32cb91d5e3797.txt`
equals the first 24 hex digits of sha256 of the URL string
`https://www.rfc-editor.org/rfc/rfc7089.txt`. No network fetch performed.

## Result: CONFIRMED (string-hash claim holds)

- **Computed sha256 (full):** `d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0`
- **First 24 hex digits:** `d0c4a09a9de32cb91d5e3797`
- **Capture file name (stem):** `d0c4a09a9de32cb91d5e3797` (file `d0c4a09a9de32cb91d5e3797.txt`)
- **Comparison:** exact string match → `MATCH: yes`

## Command used

```sh
printf '%s' 'https://www.rfc-editor.org/rfc/rfc7089.txt' | sha256sum
```

Independent cross-check (agrees byte-for-byte):

```sh
python3 -c "import hashlib; print(hashlib.sha256(b'https://www.rfc-editor.org/rfc/rfc7089.txt').hexdigest())"
# d0c4a09a9de32cb91d5e37971b546f2c380d0a60581c6bb80fb9ef72d97743d0
```

Exact comparison check:

```sh
h=$(printf '%s' 'https://www.rfc-editor.org/rfc/rfc7089.txt' | sha256sum | cut -d' ' -f1)
f=d0c4a09a9de32cb91d5e3797
# "${h:0:24}" == "$f"  →  MATCH: yes
```

Note on method: `printf '%s'` (not `echo`) guarantees no trailing newline is hashed,
so this is sha256 of the bare URL string. Both tools (`sha256sum`, Python
`hashlib`) produced the identical digest.

## Side finding: the capture file is absent from the repo

A filesystem sweep found no copy of the file:

```sh
find /home/vgpnk/Projects/shokunin/chousa-shokunin -name 'd0c4a09a9de32cb91d5e3797*'
# (no output, exit 0)
```

A Glob pass (respecting ignore files) also found no match, so this is not merely
an ignore-file artifact. Interpretation: the name convention is verified against
the hash, but the capture artifact `d0c4a09a9de32cb91d5e3797.txt` itself is not
present anywhere under the chousa-shokunin working tree. If round-44 state
asserts this capture was landed, the file is missing or lives outside the repo
(e.g. an external cache). No fetch was performed, per instructions, so the
remote-side existence could not be checked.

## What was not done

- No HTTP fetch of the URL.
- No hash of file *contents* — the claim under test concerns the URL *string*,
  and the file does not exist locally to hash anyway.
- No writes outside this report; no lane production files, git, or jj touched.
