# ReviewQuarMap — r49 w1 — absent-defect register ↔ theme-document mapping

Leaf reviewer; axes attacked: depth (mapping saturation), calibration (id-space traps).
No tools installed (none needed; host pacman pause untouched). No network; on-disk artifacts only.
Scratch `/tmp/chousa-r49-ReviewQuarMap/` deleted at end. Only write: this report.

## 1. Section-10 slice re-derived (addendum item 10, lane-addendum.md:380)

    R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
    awk -F'|' -v l='chousa' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' "$R" > /tmp/chousa-r49-ReviewQuarMap/quarantine-slice

Result: 24 lines, every line carries an S-id (`grep -c 'S[0-9]'` → 24) — matches the addendum's
2026-10-24 count "chousa 24" (lane-addendum.md:383). Per data row, id + URL ($6; the four
no-locator rows carry no URL — their register cited-source cell is shown verbatim):

    S077 https://doi.org/10.1186/s13643-020-01542-z          S093 https://aclanthology.org/2026.findings-acl.19.pdf
    S080 https://std.samr.gov.cn/gb/search/gbDetailed?id=4507EFE13D37CB6AE06397BE0A0A601F   S094 https://ojs.aaai.org/index.php/AAAI/article/download/29825/31432
    S082 https://support.nii.ac.jp/ja/cir/manual_articles_detail   S095 https://www.zcmu.edu.cn/__local/2/33/FC/FFA702D0F9381C8224BD74CB435_0E777725_C3A00.doc?e=.doc
    S084 https://www.jstage.jst.go.jp/static/pages/FAQs/TAB2/-char/ja   S096 https://jc.hit.edu.cn/_upload/article/files/f7/54/711916924125a0682e3bc3ebb6ed/1f6f2731-8c87-4812-b7e2-9fad0069d508.doc
    S086 https://www.ncpssd.cn/                              S104 https://www.jstage.jst.go.jp/article/kenkokyoiku/32/2/32_320208/_pdf/-char/ja
    S088 https://xuebaobangong.jmu.edu.cn/zkb/Upload/Park/64b9ba1b-df55-4309-87d4-0d037a497bd0.pdf   S105 https://jaohfa.com/pdf/systematic_review.pdf
    S108 https://arxiv.org/html/1803.05355                   S110 https://aclanthology.org/2025.coling-main.108.pdf
    S111 https://www.slarc.org.cn/dwyx/EN/article/downloadArticleFile.do?attachType=PDF&id=5290   S112 https://www.slarc.org.cn/dwyx/CN/article/downloadArticleFile.do?attachType=PDF&id=5237
    S114 https://www.sinomed.ac.cn/article.do?ui=2026335073  S116 https://aclanthology.org/N18-1074.pdf
    S120 https://c2h.niph.go.jp/tools/system/Reporting_Format_Jap_202404.docx   S125 http://www.gcpunion.org/upload/cmsfile/1703404975484107.doc
    S100`–S103` (register:269-272): cited-source cell = `#### Gate — S100` … `#### Gate — S103` — no URL in the row.

Calibration: register `## By lane` says chousa **20** (register:238) — stale, exactly the 4
never-checked rows short; the addendum's "totals are stale — derive your slice yourself"
(lane-addendum.md:369-370) is correct; the register header says a failed match is "a CANDIDATE,
not a verdict" (register:5-8).

## 2. Which register rows name the nine theme URLs (c2-count.py:51-61 DOCS)

Substring census over the whole register (`grep -c`, whole file):
`ForPublishers:0  EJ1372738:0  cnki-kns80:0  c1b0fa89:0  manual_articles_detail:1  FAQs/TAB2:1  ncpssd:1  zcmu:1  jc.hit.edu.cn:1`

| theme doc (staged→lane id, entry) | URL | register row |
|---|---|---|
| S087→S096 aggregator-vs-source-r36 | support.nii.ac.jp/ja/cir/manual_articles_detail | **S082** (register:39) |
| S088→S097 aggregator-vs-source-r36 | jstage ForPublishers/TAB2 | none |
| S089→S098 aggregator-vs-source-r36 | jstage FAQs/TAB2 | **S084** (register:40) |
| S091→S099 aggregator-vs-source-r36 | ncpssd.cn | **S086** (register:41) |
| S092→S100 aggregator-vs-source-r36 | eric.ed.gov/?id=EJ1372738 | none |
| S100→S101 citation-count-semantics-r37 | zcmu.edu.cn …C3A00.doc | **S095** (register:45) |
| S101→S102 citation-count-semantics-r37 | jc.hit.edu.cn …d508.doc | **S096** (register:46) |
| S102→S103 citation-count-semantics-r37 | toho-shoten cnki-kns80.pdf | none |
| S103→S104 citation-count-semantics-r37 | um.edu.mo c1b0fa89….pdf | none |

5 of 9 theme URLs have register rows. The other 4 have none because the register lists only
census-check failures (register:5-8) — those four documents produced no failed quote at census
time. Absence from the register is a clean bill, not a defect.

## 3. The four "no locator" rows S100-S103 (register:269-272)

Register cell shape: `| `chousa` | round3 | S100` | the gate block named no locator, so no
quote was checked | #### Gate — S100 |` — the cited-source cell is the register builder's
truncated finding detail (`detail=head[:80]`), not a locator (QuarantineS102.md).

What they refer to — census-time round-3 **own-work** rows
(`git -C /home/vgpnk/Projects/shokuknow show 9e91e504:lanes/chousa/round3/SOURCES-PROPOSED.md:30-33`):

- S100 = chain-hop resolution entry — `corpus/knowledge/chain-resolution-r3.md` (sha256 prefix d794343f8528e263, 15,772 B)
- S101 = citation-chain fidelity entry — `corpus/knowledge/citation-chain-fidelity-r24.md` (b4e5d36cafde9250, 8,931 B)
- S102 = exempt-hop audit entry — `corpus/knowledge/exempt-hop-audit-r32.md` (fdc55c65d8ed94c5, 3,515 B)
- S103 = revision-binding entry — `corpus/knowledge/revision-binding-r31.md` (845ea270d8e56b4b, 4,259 B)

Each Gate names `URL (repository locator): https://github.com/VeigaPunk/shokunin` +
`Local artifact: `chousa-shokunin/corpus/knowledge/<file>`` (SOURCES-PROPOSED.md@9e91e504:35-37,
45-47, 54-56, 62-64). The checker's `URL_LINE_RE` requires `URL\s*[:=]`, so `URL (repository
locator):` fails, and `local_locator()` resolves the repo-relative path against `lane_dir`,
never the fleet root → "no locator" (QuarantineS102.md mechanism section). None of the four
names any of the nine theme URLs; the only URL is the non-binding github repository locator.

Verdict history: round-42 spotcheck ruled the family `unverifiable`
(round-42-verifier-spotcheck.md:121 — "register unchecked family, class cell names no
locator"); round-48 hand-check **superseded** it — all four present (round-48.md:62-65: pinned
artifacts match digest/size, all quote spans resolve; parser defect, not a source defect).

## 4. Was any theme document's register row ruled fabricated/unverifiable?

**No.** Round-48 verdict table (round-48.md:43-66, the closure's 24/24): S082
absent-as-written (:44), S084 absent-as-written (:45), S086 present (:46), S095
absent-as-written (:50), S096 absent-as-written (:51); S100-S103 present (:62-65). No
theme-URL register row carries `fabricated` or `unverifiable`. The register's own class cell
for the five URL rows is `payload-absent` (the fabrication class), but that is a candidate
label (register:5-8), and the counter fixes verdict truth with the closure ("Verdict-line
truth is the closure's", c2-count.py:29). The only `unverifiable` ruling ever attached to
register ids S100-S103 (round-42) attaches to own-work rows, not theme documents; round-48
byte evidence supersedes it.

## 5. Does c2-count's URL-based register mapping miss any theme row?

**No.** Counter ground truth (ran `python3 …/corpus/evidence/round49/c2-count.py`):

    QUARANTINE_VERDICTS=0/5 (S082,S084,S086,S095,S096)   QUARANTINE_BLOCKED_ADOPTED=0   C2=FAIL (build-stage expected)

The counter's pool (c2-count.py:200-207: `chousa` in f[1], round in f[2], S-id in f[3],
`url_of(f[5])` ∈ theme) spans all 24 slice rows and maps exactly the 5 URL-bearing theme rows.
Saturation: the §2 substring census found each of the 5 URLs exactly once in the whole
register and the other 4 theme URLs zero times — no theme URL hides in another cell, another
lane's row, or a malformed row. The four no-locator rows are invisible to URL-mapping but are
own-work rows (§3), not theme rows — correctly excluded, not missed. When all 9 docs bind,
`blocked` stays 0 because no theme-row verdict is fabricated/unverifiable (§4; c2-count.py:213-215).

## 6. Calibration traps for the entry drafters (actionable)

- Three id namespaces collide by design: register S088 = xuebaobangong PDF vs staged S088 =
  jstage ForPublishers — unrelated documents; register S095/S096 (zcmu/hit) ≠ staged
  S095/S096; register S100-S103 (own-work) ≠ staged S100-S103 (zcmu/hit/toho/um). The counter
  maps by URL, never by id arithmetic.
- Round-49 lesson verdict lines MUST name register ids S082/S084/S086/S095/S096 (VERDICT_RE
  c2-count.py:68; match gate c2-count.py:211). Verdict lines keyed to staged ids (S087-S103)
  or lane ids (S096-S104) silently drop out → QUARANTINE_VERDICTS=0/5 → C2=FAIL.
- Natural verdicts from round-48: S082/S084/S095/S096 absent-as-written, S086 present —
  absent-as-written still binds the document (the misquote is the register's; content is in
  the capture), so none of the five blocks adoption.
- Register round labels are census-time numbering (QuarantineS100.md: "readers matching it against current files will mis-bind").

VERDICT: mapped the 24-row chousa register slice to the nine theme URLs — 5 rows (S082/S084/S086/S095/S096) carry theme URLs, 4 theme URLs have no register row (clean at census), the four no-locator rows S100-S103 are round-3 own-work artifacts (github locator + lane-local sha256 pins), no theme row was ruled fabricated/unverifiable, and c2-count's URL-based mapping misses no theme row (counter: QUARANTINE_VERDICTS=0/5 (S082,S084,S086,S095,S096)).
