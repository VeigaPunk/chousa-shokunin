# AttackRowS059 — source row S059 (Python hashlib) and its quote

Seat: ChousaR31.AttackRowS059 (wave 2 falsify, round 31). Lane tip `ee1024f`. No lane file
edited; scratch: `/fast/scratch/hyaku/chousa-r31/w2/AttackRowS059/`.

Disclosure: analysis imported `tools/quote-reopen.py` via `importlib`, which created
`tools/__pycache__/quote-reopen.cpython-314.pyc` (01:48:03). It was deleted immediately
(`rm`, then `rmdir`), and `git status --porcelain` no longer lists `tools/__pycache__/`.
No tool or production bytes were changed.

## What was attacked

1. The S059 row in `corpus/SOURCES.md:69` (scope / teaches / anchor cells, kind, tier).
2. The quote carried in `.ufo/waves/round-31/build/ScribeSrcHashlib/drafts.md`:
   `Like digest() except the digest is returned as a string object of double length, containing only hexadecimal digits.`
3. The lane tool `tools/quote-reopen.py verify` on that quote with a one-item TSV.

## GET receipt (one direct GET, no redirect followed)

`python3 fetch_once.py` (stdlib `http.client`, cert verification on), exit 0:

- `HTTP/1.1 200 OK`, `Location=None` (no redirect), `Content-Type: text/html`,
  `Content-Encoding=None`.
- `bytes=121928`, `sha256=553f4f2a9e686e6f051c8b12bd5469e7fdd6cc7116b2f6d2beba68c1a703af10`.
- `Date: Fri, 23 Oct 2026 04:47:52 GMT`, `Last-Modified: Fri, 23 Oct 2026 01:40:01 GMT`.
- Body saved at scratch `response.body`; headers at `response.headers`.

Comparison: the build seat's captured body
`.ufo/waves/round-31/build/ScribeSrcHashlib/response.body` is byte-identical (same 121,928
bytes, same SHA-256). So the page did not change between the draft and this attack, and the
draft's "opened-body evidence" numbers are true.

## Verbatim check (whitespace-folded)

- Quote words: **18** (limit 25).
- Raw HTML has **0** byte-exact occurrences (Sphinx wraps `digest()` in markup and wraps the
  sentence across a newline: `...string object of\ndouble length...`).
- One `<p>` at body bytes **42398–42788** (inclusive), `Like` at byte **42401**:
  `<p>Like <a ...>digest()</a> except the digest is returned as a string object of\ndouble length, containing only hexadecimal digits.  This may be used ...</p>`
- After whitespace folding the sentence is present exactly; normalized page text offset 7395.
- It occurs **twice** on the page: `hash.hexdigest()` (this one, byte 42663 region) and
  `shake.hexdigest(length)` (byte 47170 region) carry the identical sentence. The quote alone
  therefore does not distinguish the two; the row's anchor names the hash-object method.

**Verdict: verbatim yes (whitespace-folded), 18 words.**

## Lane tool verdict

```
python3 tools/quote-reopen.py verify --items .ufo/waves/round-31/falsify/AttackRowS059/items.tsv
QUOTE_REOPEN	S059	VERBATIM	matched in normalized page text
QUOTE_REOPEN_SUMMARY verbatim=1 absent=0 too_long=0 no_source=0 unreachable=0
exit 0
```

(First run used a TSV whose source column was ` S059` and returned `NO_SOURCE`; that was the
seat's TSV typo, re-run corrected. Output in `items.tsv` and `quote-reopen.out` beside this
report.) The tool fetches the registry URL itself; that is its own GET to the same allowed URL.

## Row cells against the page

| Cell | Check | Evidence |
|---|---|---|
| kind `docs` | holds | It is the official Python standard-library reference page. |
| tier `A` | holds by precedent | Official Python docs, same basis as S038/S044/S049/S052–S056 and QUALITY criterion 7 (tier A or B); the row's own scope is narrow and does not lean on it for a lowercase rule. |
| scope | holds | Page: "feed this object with bytes-like objects (normally bytes) using the update method"; "digest of the concatenation of the data fed to it so far"; hexdigest is "hexadecimal digits". No text-encoding rule and no hexdigest-case rule on the page. |
| anchor `Hash algorithms` | holds | `<h2>Hash algorithms` at body byte 13852. |
| anchor `Hash Objects` | holds | `<h2>Hash Objects` at body byte 38052 — capital O, matching the row. |
| anchor ids | holds | `id="hashlib.hash.digest_size"`, `hashlib.hash.update`, `hashlib.hash.digest`, `hashlib.hash.hexdigest` each occur once; `hashlib.sha256` occurs once. |
| anchor version | holds | Page banner: "Python » 3.15.1 Documentation". |
| anchor date | holds | `Date` header 2026-10-23; body hash equal to the build capture. |
| teaches, part 1 | holds | "use sha256() to create a SHA-256 hash object ... feed this object ... using the update method ... digest of the concatenation of the data fed to it so far". |
| teaches, part 2 | holds | "returned as a string object of double length, containing only hexadecimal digits"; `digest()` is "a bytes object of size digest_size"; `digest_size` is "The size of the resulting hash in bytes". |
| teaches, case absence | holds | The only `lowercase` on the page is about `hash.name` ("always lowercase"), not hexdigest; `upper`, `capital`, `ASCII` occur 0 times. |

## Corrections

**None required.** One optional precision, not a defect: the page says "bytes-like objects
(normally bytes)" where the scope cell says "for bytes fed to a hash object"; tightening to
"bytes-like" would mirror the page, but the scope cell is a declared limitation and does not
misattribute anything to the page.

## Incidental observation (not S059's defect)

The corpus points at a tier legend that is not in the lane: `corpus/QUALITY.md:13` says tier
definitions live in `corpus/SOURCES.md` (contract v1), but SOURCES.md has no legend, and
`corpus/README.md:54` cites `kaika/SOURCES-CONTRACT-v1.md`, which is absent from the fleet tree
(`find /home/vgpnk/Projects/shokunin -maxdepth 3 -name SOURCES-CONTRACT-v1.md` → empty). Tier A
here was therefore judged by the registry's own docs precedent, not by a written legend.

## Limits

- The tool proves normalized occurrence, not byte-identity: the raw sentence is split by a
  newline, so "VERBATIM" is a whitespace-folded result by design.
- The quote is not unique on the page (same sentence under SHAKE's `hexdigest(length)`), so the
  tool alone cannot prove the row points at the hash-object paragraph; the anchor text does.
- Network: one direct GET plus the tool's fetch, both to `docs.python.org` only; no redirect
  was followed by the direct GET (`Location=None`). The page may change after 2026-10-23.
- No `lsp` use: this is a documentation page with no code definition to resolve; semantic
  symbol checks were done on the page's Sphinx ids instead.
