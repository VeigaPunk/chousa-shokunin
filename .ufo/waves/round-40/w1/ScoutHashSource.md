# ScoutHashSource — round 40, wave 1 (scout)

## Assigned attack

Re-open S059's official Python `hashlib` documentation at the recorded anchor, confirm the quoted digest semantics and 2026-10-24 access, and assess whether the note avoids claiming truth or authorship from a hash.

This seat's dispatch item is itself the re-open (`.ufo/waves/round-40/w1-spec.json`, item `ScoutHashSource`); the fetch is a single read-only GET of the public docs URL, authorized by that item — the same pattern round 31 used when S059 was first mined (`SentinelFetchScope` item, same spec).

## Exact command and output

Command (one live GET, today 2026-10-24):

```
read https://docs.python.org/3/library/hashlib.html#hash-algorithms
```

Observed (verbatim from served page, section "Hash algorithms"):

> There is one constructor method named for each type of *hash*. All return a hash object with the same simple interface. For example: use `sha256()` to create a SHA-256 hash object. You can now feed this object with bytes-like objects (normally `bytes`) using the `update` method. At any point you can ask it for the *digest* of the concatenation of the data fed to it so far using the `digest()` or `hexdigest()` methods.

Page `<title>`: `hashlib — Secure hashes and message digests — Python 3.15.1 documentation`.

Corroboration commands:

- `grep -c 'concatenation of the data fed to it so far' .ufo/waves/round-31/build/ScribeSrcHashlib/response.body` → `1` (the pinned round-31 fetch receipt body at `response.body:258` carries the same sentence; the recorded 2026-10-23 access predates this round, so the anchor paragraph has not drifted between the two accesses).
- `printf 'the digest of the concatenation of the data fed to it so far' | wc -w` → `13` (matches the lesson's declared 13-word located quote).

## Findings

1. **Anchor resolves** (agree). `#hash-algorithms` lands on the "Hash algorithms" section; the paragraph beginning "There is one constructor method named for each type of hash" is present and unchanged vs the pinned round-31 body (`response.body:251-259`).
2. **Quoted digest semantics confirm** (agree). The 13-word quote "the digest of the concatenation of the data fed to it so far" is an exact substring of the live page and of the pinned copy. Supporting semantics in the same page also hold as S059's row describes: `hash.update` — "Repeated calls are equivalent to a single call with the concatenation of all the arguments"; `hash.hexdigest()` — "a string object of double length, containing only hexadecimal digits" (letter case unspecified, matching the row's caveat). Page version is `Python 3.15.1`, matching the row's anchor cell.
3. **2026-10-24 access confirmed** (agree, as a re-open record). This seat fetched the page live on 2026-10-24 and the anchor text still says what the lesson records (`corpus/lessons/round-40.md:40-41`). The S059 row's `opened`/`recheck` cells deliberately remain `2026-10-23`/`on-release` — the lesson states "status and recheck are unchanged" — so the 2026-10-24 date lives in the lesson and in the note's `verified-at:` field, not in the row. That asymmetry is consistent, not an error.
4. **Note avoids claiming truth or authorship** (agree). `corpus/knowledge/receipt-expectation-digests-r40.md` claims only that `expect_sha256` "binds the exact file bytes." Its `## Limit` (lines 17-19) states: "A matching file digest establishes byte identity for the supplied input; it does not establish the truth of a claim, the authority of a source, or who authored a receipt." The lesson's rejected-claim entry (`round-40.md:47`) explicitly rejects "SHA-256 proves receipt authorship or semantic truth." S059's own scope cell disclaims the same overreach ("not a general SHA-256 text-encoding standard, lowercase-output requirement, or the lane's revision-pin contract").
5. **Local application is accurate.** The note cites `corpus/evidence/round39/verify-receipts.py:73-79,138-139`: `sha256_file` streams the file through `update()` in 65536-byte chunks and returns `hexdigest()` (73-78); `expect_sha256` is compared to `sha256_file(args.expectations)` at 138-139, and the failure `expect-sha256-mismatch` precedes scenario census re-derivation (census load at 87-97 is invoked only after the digest gates at 128-139 pass). "Binds whole-file bytes, not only cited rows" follows.
6. **Residual nuance (below defect threshold).** "Byte identity" rests on SHA-256 collision resistance — equality shows identical inputs to a very high practical bound, not a logical proof of byte equality; and identity of the *file* does not itself bind the receipt author. The note does not state this assumption, but it also never claims stronger than byte identity, so the omission is calibration, not overclaim. Also observed: unlike round 31 (`fetch_sources.py` + `sources/receipts.json`), round 40 committed no fetch receipt for the re-open; today's content is corroborated only by the round-31 pinned body and this seat's live read. Acceptable for a read-only audit, worth knowing if a future round needs byte-pinned provenance.

## Verdict

**Agree.** S059 re-opens cleanly at the recorded anchor on 2026-10-24; the 13-word digest-concatenation quote is verbatim on the live page (still Python 3.15.1); the knowledge note limits the digest to byte identity and expressly disclaims truth, authority, and authorship; the cited verifier lines do what the note says. No counterexample found; the only residual is an unstated collision-resistance assumption and the lack of a committed round-40 fetch receipt.

## Artifact pointers

- Live URL (fetched 2026-10-24): `https://docs.python.org/3/library/hashlib.html#hash-algorithms`
- Pinned prior fetch: `/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-31/build/ScribeSrcHashlib/response.body:251-259` (headers in same dir)
- Source rows: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:69` (S059), `:84` (S074 rejected duplicate), `:106-109` (registry search log)
- Lesson gate: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/lessons/round-40.md:32-51`
- Knowledge note under review: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/knowledge/receipt-expectation-digests-r40.md` (observation :11-15, limit :17-19)
- Local application: `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round39/verify-receipts.py:73-78,87-97,128-139`

## Tooling

No installs or updates performed; pacman untouched (paused host-wide). One authorized external GET (this seat's dispatch item).
