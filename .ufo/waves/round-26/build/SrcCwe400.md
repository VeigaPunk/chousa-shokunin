# CWE-400 source opening — round 26

Axes: quote fidelity; registry-contract fit; scope honesty.

## Observed
- Primary URL opened: `https://cwe.mitre.org/data/definitions/400.html`; HTTP outcome `200`, effective URL unchanged (`curl -sS -o /dev/null -w '%{http_code} %{url_effective}\n' ...` → `200 https://cwe.mitre.org/data/definitions/400.html`). No mirror needed. Page title identifies CWE-400, version 4.20; opened 2026-10-21.
- Verbatim quote (14 words), CWE-400 `Description` section: “The product does not properly control the allocation and maintenance of a limited resource.” Raw-page check found the exact sentence. The entry labels CWE-400 an Abstraction: Class. Its `Relationships` table lists `ParentOf` CWE-770, a Base named “Allocation of Resources Without Limits or Throttling.” `Vulnerability Mapping Notes` says use is DISCOURAGED for mapping real-world vulnerabilities, warns against conflating the weakness with technical impact, and advises analyzing the specific mistake/considering children. (Source: exact URL above; sections `Description`, `Relationships`, `Vulnerability Mapping Notes`.)
- Current registry duplicate check: `functions.grep` with pattern `(?i)cwe|mitre` on `corpus/SOURCES.md` → no matches. `corpus/SOURCES.md:9` gives the v1 11-column header; `:44` now has S034 for reader-allocation own-work, not this source. Keep the proposed id TBD; allocate an unused id at integration. Contract: `CORPUS.md:64-122` (v1 shape, tier/status and row rules).
- C1 is the bounded metadata-header reader claim; the pre-registration records the 8,388,000-byte newline-only case and per-line array amplification (`corpus/evidence/round26-claims.md:26-32`).

## Proposed SOURCES.md row (contract v1 order)
| TBD | MITRE CWE-400: Uncontrolled Resource Consumption (4.20) — https://cwe.mitre.org/data/definitions/400.html | docs | A | MITRE's authoritative taxonomy record for its own CWE-400 class and child relationships only; not authority for classifying this gate | Description; Relationships (ParentOf CWE-770); Vulnerability Mapping Notes; CWE 4.20 as served 2026-10-21 | CWE-400 is a class for improper control of limited-resource allocation/maintenance; CWE-770 is its Base child for allocation without limits/throttling; analyze the concrete mistake, not resource-consumption impact alone | queued | 2026-10-21 | 180d | — |

Queued because the source is opened and relevant but no knowledge entry cites this proposed row; flip to mined when a citing entry is named in `used-by`. Tier A is limited to MITRE's own taxonomy statements. `180d` is proposed to revisit the versioned entry.

## Scope limits
- The page does not establish that the gate's behavior is a security vulnerability, verify the C1 measurements, or prescribe Bash/line-array implementation or a memory budget. Its mapping note explicitly cautions against using CWE-400 for real-world vulnerability mapping.
- CWE-770 is listed as a more specific child for allocation without limits/throttling; this page alone does not establish that C1 meets that mechanism or justify assigning CWE-770. Any use outside the row's scope is an inference and must be labeled (QUALITY 7); source opening/topic/statement do not by themselves prove a claim true (QUALITY 8), `corpus/QUALITY.md:24-32`.
- It does not support C2 freshness rules or C3 registry-calibration checks.

Installs: none.
VERDICT: Opened official primary page (HTTP 200); useful for the CWE-400/CWE-770 taxonomy distinction only, with no duplicate registry row.