# SourcesDraft evidence — verbatim command outputs (2026-10-30)

All commands read-only; cwd fleet root or seat scratch (deleted after). Collected from tool transcripts unedited.

## Hashes (sha256sum)

```
8eb0bb079fa0cdf682920d0327fc1e72d5704961c9c54cdc716909251efd5737  /usr/share/man/man1/git-cat-file.1.gz
88fa624821fbdee7eb2ef87c2437b207afe328cf117c7463367e2db5eb1af492  /usr/lib/python3.14/hashlib.py
ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b  /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round64/controls/c1v3-before-full.txt
```

All three equal the `sha256` fields in corpus/evidence/round65/source-openings.json.

## S154 — git-cat-file(1)

```
$ zcat /usr/share/man/man1/git-cat-file.1.gz | grep -n -F 'raw (though uncompressed) contents'
505:If \fI<type>\fR is specified, the raw (though uncompressed) contents of the \fI<object>\fR will be returned\&.

$ zcat /usr/share/man/man1/git-cat-file.1.gz | grep -n '^\.SH'
30:.SH "NAME"
32:.SH "SYNOPSIS"
44:.SH "DESCRIPTION"
53:.SH "OPTIONS"
495:.SH "OUTPUT"
506:.SH "BATCH OUTPUT"
719:.SH "CAVEATS"
726:.SH "GIT"

$ zcat /usr/share/man/man1/git-cat-file.1.gz | grep -m1 '^\.TH'
.TH "GIT\-CAT\-FILE" "1" "2026\-09\-27" "Git 2\&.56\&.0" "Git Manual"

$ MANWIDTH=1000 man -l /usr/share/man/man1/git-cat-file.1.gz | col -bx | grep -n '^OUTPUT$'
150:OUTPUT

$ MANWIDTH=1000 man -l /usr/share/man/man1/git-cat-file.1.gz | col -bx | grep -n -F 'raw (though uncompressed)'
159:     If <type> is specified, the raw (though uncompressed) contents of the <object> will be returned.
```

Note rendered line 159 contains `the <object> will be returned`; the drafted quotes read `the object will be returned` (finding 1 in the report).

## S155 — hashlib.py

```
$ python3 --version
Python 3.14.8

$ sed -n '28,36p' /usr/lib/python3.14/hashlib.py
 - update(data): Update the hash object with the bytes in data. Repeated calls
                 are equivalent to a single call with the concatenation of all
                 the arguments.
 - digest():     Return the digest of the bytes passed to the update() method
                 so far as a bytes object.
 - hexdigest():  Like digest() except the digest is returned as a string
                 of double length, containing only hexadecimal digits.
 - copy():       Return a copy (clone) of the hash object. This can be used to
                 efficiently compute the digests of data that share a common
```

Quoted span "Return the digest of the bytes passed to the update() method" is wholly on line 31; sentence continues on line 32.

## S156 — c1v3-before-full.txt

```
$ wc -l -c < .../controls/c1v3-before-full.txt
     44    1505
$ tail -c 1 ... | xxd
00000000: 0a
line 1: LEG CLEAN clean ok ok
line 44: CLEAN=1/1 DEFECTS=17/28 BENIGN=8/11 ZERO=3/3 BATTERY=FAIL
```

No line in the file contains REVISION, EXIT or SHA256 header fields (full 44-line read).

```
$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show d6ed8155e9b4735639a2cf0a3e479c62f2056195:corpus/evidence/round64/controls/c1v3-before-full.txt | sha256sum
ca05f579dc0f979a772ecec973a1da5d5df8d11881ca678708c72044f8c9c05b  -
```

Identical to the working-tree file: the row cell "at base d6ed8155e9b4735639a2cf0a3e479c62f2056195" is byte-accurate.

## Package provenance and git state (read-only)

```
$ pacman -Qo /usr/share/man/man1/git-cat-file.1.gz
/usr/share/man/man1/git-cat-file.1.gz is owned by git 2.56.0-1
$ pacman -Qo /usr/lib/python3.14/hashlib.py
/usr/lib/python3.14/hashlib.py is owned by python 3.14.8-1
$ pacman -Q git python
git 2.56.0-1
python 3.14.8-1

$ git -C /home/vgpnk/Projects/shokunin/chousa-shokunin status --porcelain -- corpus/SOURCES.md corpus/knowledge/receipt-identity-r65.md corpus/lessons/round-65.md corpus/README.md corpus/evidence/round65/
 M corpus/README.md
 M corpus/SOURCES.md
?? corpus/evidence/round65/source-openings.json
?? corpus/knowledge/receipt-identity-r65.md
?? corpus/lessons/round-65.md
```

## Registry rows observed (SOURCES.md uncommitted lines 164–167, abridged cells)

- `| S154 | git-cat-file(1) — installed /usr/share/man/man1/git-cat-file.1.gz | docs | A | … | OUTPUT paragraph on explicit type, Git 2.56.0 manual dated 2026-09-27 | … | mined | 2026-10-30 | on-release | corpus/knowledge/receipt-identity-r65.md |`
- `| S155 | hashlib installed module documentation — /usr/lib/python3.14/hashlib.py | code | A | … | module documentation lines27–34, Python 3.14.8 | … | mined | 2026-10-30 | on-release | corpus/knowledge/receipt-identity-r65.md |`
- `| S156 | Round64 before measurement — corpus/evidence/round64/controls/c1v3-before-full.txt | own-work | B | … | lines1–44 at base d6ed8155e9b4735639a2cf0a3e479c62f2056195 | … | mined | 2026-10-30 | on-release | corpus/knowledge/receipt-identity-r65.md |`
- `| S157 | … | own-work | C | … | rejected | 2026-10-30 | on-release | — |` (not this seat)
