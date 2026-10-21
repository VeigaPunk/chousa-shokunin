# SrcNisoJav-3 — NISO JAV source opening (round 26)

Axes: freshness (C2 release-time version signal); calibration (C3 scope of the source claim).

## Opened source and located quote
- Landing page opened at `https://www.niso.org/publications/niso-rp-8-2008-jav`; `curl -sS -o /dev/null -w '%{http_code} %{url_effective}\n' URL` returned `200 https://www.niso.org/publications/niso-rp-8-2008-jav`. The page identifies NISO RP-8-2008 and links to the official NISO-hosted PDF. No mirror needed.
- Official PDF `https://www.niso.org/sites/default/files/2017-08/RP-8-2008.pdf`: HTTP 200, 218,592 bytes, 14 pages. Extracted text `/tmp/rp8-2008.pdf:343-346` (Recommended Terms and Definitions / “Corrected Version of Record,” Definition; printed p.4, PDF p.14; RP-8-2008, April 2008): “A version of the Version of Record of a journal article in which errors in the VoR have been corrected.” (20 words.)
- Related anchors: PDF extracted lines 269-273 propose metadata identifying each document object's status and list VoR/CVoR/EVoR; lines 352-357 distinguish EVoR supplementary enhancement from correction. PDF p.2 says the practice “may be revised or withdrawn”; its current status was not established here.

## Proposed SOURCES.md row (contract v1 order)
| S034* | NISO RP-8-2008, Journal Article Versions (JAV) — https://www.niso.org/publications/niso-rp-8-2008-jav | spec | A | NISO's own recommended status terms for scholarly journal-article versions, especially VoR/CVoR/EVoR; not a recheck policy or evidence about an individual article | “Recommended Terms and Definitions for Journal Article Versions” / “Corrected Version of Record,” Definition, printed p.4 (PDF p.14), RP-8-2008 (April 2008); official PDF URL above | CVoR denotes a VoR version with errors corrected, distinct from EVoR's supplementary enhancement; a release-time check can look for declared CVoR/EVoR status (recheck policy is lane inference) | queued | 2026-10-21 | on-release | — |

`*` S001–S033 are present; S034 is next unused, subject to integrator assignment. Tier A reason: this is NISO's own recommended practice, primary for the terms it defines. Status rationale/flip: queued because it was opened and has a narrow directly grounded distinction; promote to mined only when a relevant knowledge entry cites it in `used-by`, or reject if no relevant entry can use it (reconsider rejection if such a scoped need arises). No duplicate: grep of `corpus/SOURCES.md` for `NISO|Journal Article Versions|JAV|RP-8-2008` returned “No matches found”; S028 Crossmark is a different, complementary source.

## C2/C3 use and limits (QUALITY 7/8)
- C2: a release-time freshness recheck could look for explicit VoR/CVoR/EVoR status or a correction/enhancement notice, and distinguish correction from supplementary enhancement. NISO supplies the version vocabulary and definitions, not the recheck trigger, cadence, or due-date rule; applying the vocabulary as a gate check is inference.
- C3/QUALITY 7: tier A covers only NISO's definitions/recommendation for journal-article versions. This source does not establish how every publisher labels corrections, whether a particular article has changed, what version a researcher should cite, or a general research-record freshness policy.
- QUALITY 8 states kept separate: observed page/PDF opens (HTTP 200); on-topic (journal-article versioning); source states that CVoR corrects errors in a VoR and lists the version states; no article-specific claim's truth or update status was tested. Current/withdrawn status of RP-8-2008 remains unknown; the document says to contact NISO for current status.
- `corpus/evidence/round26-claims.md` calls for a round-26-opened row in the C2 knowledge entry; this is a candidate only until the entry cites it. No installs; no source-tree edits.

VERDICT: Opened the official NISO page and practice; candidate row is narrowly useful for identifying correction/enhancement version signals, but does not itself prescribe freshness checks.
