| S063 | Python `json` documentation — https://docs.python.org/3/library/json.html#repeated-names-within-an-object | docs | A | Python 3.15.1 `json` decoder's default handling of repeated object names and the `object_pairs_hook` option to alter it; not JSON's normative requirements or this lane's top-level-field reader policy | “Repeated Names Within an Object”; `json.load()`/`json.loads()` `object_pairs_hook`; Python 3.15.1 documentation as served 2026-10-23, HTTP 200, body SHA-256 `5ceeeaf6b0c866bd413ac0a9316f92cd46e03984cfec87cf7ac051ca6235608b`; footer `Last updated on Oct 23, 2026 (07:34 UTC)` (same timestamp and body in both GETs) | Python's default decoder ignores all but the last repeated object name-value pair; `object_pairs_hook` can alter that behavior. | queued | 2026-10-23 | on-release | corpus/knowledge/claim-record-fields-r33.md |

## Fetch evidence

Command 1 (body `json-1.html`, headers `json-1.headers`):
```sh
timeout 75 curl --proto '=https' --max-redirs 0 --max-time 60 --max-filesize 1048576 -sS -D /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.headers -o /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.html -w 'HTTP_STATUS=%{http_code}\nURL_EFFECTIVE=%{url_effective}\nSIZE_DOWNLOAD=%{size_download}\n' https://docs.python.org/3/library/json.html
```
Command 2:
```sh
timeout 75 curl --proto '=https' --max-redirs 0 --max-time 60 --max-filesize 1048576 -sS -D /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-2.headers -o /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-2.html -w 'HTTP_STATUS=%{http_code}\nURL_EFFECTIVE=%{url_effective}\nSIZE_DOWNLOAD=%{size_download}\n' https://docs.python.org/3/library/json.html
```
Both requests returned `HTTP_STATUS=200`, the same effective URL, and `SIZE_DOWNLOAD=115104`.

```sh
timeout 30 sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.html /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-2.html
```
Both bodies hashed to `5ceeeaf6b0c866bd413ac0a9316f92cd46e03984cfec87cf7ac051ca6235608b`.

Exact comparison command:
```sh
timeout 30 cmp -s /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.html /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-2.html; printf 'CMP_EXIT=%s\n' "$?"
```
Output: `CMP_EXIT=0`.

Exact footer command:
```sh
timeout 30 grep -oE 'Last updated[^<]+' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-1.html; timeout 30 grep -oE 'Last updated[^<]+' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-2.html
```
Both footer lines: `Last updated on Oct 23, 2026 (07:34 UTC).`; no footer-clock variance was observed between these two GETs.
## Quote verification

Located at “Repeated Names Within an Object” in the Python 3.15.1 documentation (opened page text, lines 620–633):

> By default, this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name:

The tag-stripped text artifact `json-tag-stripped.txt` was produced from the fetched HTML using Python's `html.parser.HTMLParser` with character references converted and script/style/noscript data excluded. Exact executed command and output:

```sh
timeout 30 grep -cF 'By default, this module does not raise an exception; instead, it ignores all but the last name-value pair for a given name:' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourcePyJson/json-tag-stripped.txt
```
Output: `1`.

## Curation note

Tier A is limited to official Python documentation of Python's own decoder behavior. `corpus/knowledge/claim-record-fields-r33.md` did not exist when checked; the row is therefore `queued`, with the requested used-by path pending that knowledge entry's creation.