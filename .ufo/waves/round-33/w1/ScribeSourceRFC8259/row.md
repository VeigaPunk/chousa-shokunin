# Proposed SOURCES.md row — S062

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S062 | RFC 8259, The JavaScript Object Notation (JSON) Data Interchange Format — https://www.rfc-editor.org/rfc/rfc8259.txt | spec | A | RFC 8259’s §4 object model: members are string-name/value pairs; §3 permits object and array values; §4 recommends unique names and says duplicate-name receiver behavior is unpredictable. This is standards semantics, not this lane’s top-level `verify-claims` reader contract. | §3 “Values” lines 296–308 and §4 “Objects” lines 316–333, 343–344; RFC 8259 (December 2017), body as served 2026-10-23 (HTTP 200, 28,360 bytes, SHA-256 `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7`) | Distinguish RFC semantics from a local record-reader contract: object members pair names with values, including nested objects and arrays; unique names are recommended because duplicate-name receiver behavior is unpredictable. | mined | 2026-10-23 | 365d | corpus/knowledge/claim-record-fields-r33.md |

## Opened-source evidence

Fetched only the assigned registered URL with GET; curl did not follow redirects:

```sh
timeout 60s bash -c 'mkdir -p /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourceRFC8259 && curl --silent --show-error --max-time 30 --output /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourceRFC8259/rfc8259.txt --write-out "HTTP_STATUS=%{http_code} BODY_SIZE=%{size_download}\n" https://www.rfc-editor.org/rfc/rfc8259.txt && sha256sum /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourceRFC8259/rfc8259.txt && wc -l /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourceRFC8259/rfc8259.txt'
```

Output: `HTTP_STATUS=200 BODY_SIZE=28360`; `61a5378f4255c720beb2a4b4a63b29540147c140f36988bf086291989b4cd2d7  rfc8259.txt`; `899 rfc8259.txt`.

1. §4, body line 322 (8 words): “The names within an object SHOULD be unique.”
   ```sh
   grep -cF 'The names within an object SHOULD be unique.' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourceRFC8259/rfc8259.txt
   ```
   Output: `1`.
2. §4, body line 333 (8 words; the two spaces are present in the fetched text): “unpredictable.  Many implementations report the last name/value pair”
   ```sh
   grep -cF 'unpredictable.  Many implementations report the last name/value pair' /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-33/w1/ScribeSourceRFC8259/rfc8259.txt
   ```
   Output: `1`.

The §4 grammar at lines 318–327 defines object members as name/value pairs (`member = string name-separator value`); §3 line 308 defines `value` to include `object` and `array`. The knowledge target was not present in the corpus/knowledge listing when inspected; the mined status and used-by are the requested linkage, pending that entry’s completion. This RFC does not specify the lane’s claim-record field schema or prescribe its duplicate-field rejection implementation.