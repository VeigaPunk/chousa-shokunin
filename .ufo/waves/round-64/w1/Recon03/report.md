# Recon03 — current chousa quarantine slice (advisory)

## Scope and axes
Axes: provenance accuracy, slice completeness, namespace safety, zero adoption/mutation. Read-only documentary recon; no adoption, production changes, execution probes, network fetches, clone, or scratch tree. Only L1 may integrate. No tool installations/updates; version/channel/reason: not applicable.

## Observed findings — high confidence

1. **Current register data yields 24 chousa rows, not its summary's 20.** Source: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`, data lines 37–56 and 269–272; stale summary line 238. Independently enumerating both table shapes gives:

| Register class | IDs | Count |
|---|---|---:|
| `payload-absent` candidates | S077, S080, S082, S084, S086, S088, S093, S094, S095, S096, S104, S105, S108, S110, S111, S112, S114, S116, S120, S125 | 20 |
| Never checked: gate block named no locator | S100, S101, S102, S103 | 4 |

The unchecked rows carry a trailing Markdown backtick after their identifier; strip that formatting, not the row. Register lines 6–14 explicitly call unmatched quotes candidates requiring hand verification; lines 256–261 forbid treating unchecked rows as fabrications. This is a current documentary derivation, not a re-executed capture adjudication.

2. **The merge report is staging metadata, not authorization or current lane state.** `/home/vgpnk/Projects/shokuknow/merge/chousa/MERGE-REPORT.md:3–13` says nothing was written into the lane, lists 114 accepted proposed rows, zero refused, 58 entries, and a packaging-time 81-row lane with first staged ID S082. Its checklist at lines 108–117 requires Gate reading and spot reopening before append. `accepted` here does not establish source truth or present adoption readiness. Rows S170/S171 are explicitly queued because no proposed entry cites them (lines 78–85).

3. **Campaign register IDs, staged IDs, and held lane IDs are different namespaces.** The register's S077 is the PRISMA-S DOI. The present package `/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md:7` assigns that document S082. The held lane `/home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md:87,92` uses S077 for the Poppler manual and S082 for AVeriTeC. Thus the actual first staged ID collides with a different current lane document. Do not resolve quarantine by matching bare IDs against current lane rows, or adopt by blind arithmetic. This finding establishes a concrete collision, not an exhaustive collision census. The older lesson `corpus/lessons/round-42.md:141–149` described a then-first staged S077; that historical boundary is not the present package's S082 boundary.

4. **Inherited offline verdicts are not today's source checks.** `corpus/evidence/round59/quarantine-slice-rederived.tsv:1–24` contains the same 24 register IDs. `corpus/evidence/round59/quarantine-verdict-lane.txt` records 14 absent and 10 unverifiable: absent S080/S082/S084/S088/S093/S094/S104/S105/S108/S110/S111/S112/S114/S116; unverifiable S077/S086/S095/S096/S120/S125/S100/S101/S102/S103. `corpus/lessons/round-59.md:18–22` expressly limits this to lane-owned captures and no live fetch. Round42 instead recorded 15 absent/9 unverifiable (`corpus/lessons/round-42.md:58–75`); do not promote that older split over round59 or describe either as a fresh current-origin adjudication.

## Lane slice / inference

The relevant slice remains those 24 campaign rows, bound to their cited documents and campaign rounds. Adoption remains closed for this seat and is explicitly none in `corpus/lessons/round-64.md:35`. The strongest safe next integration input is the full 24-row documentary slice plus the concrete namespace collision, not a claim that the package is cleared. A later adoption decision needs document-bound mapping, source reopening under operator scope, and citation repointing; this seat performs none of those actions.

## Frozen-claim boundary

Read `corpus/evidence/round64/claims.md` first after mandatory rules. Its C1 kill rule (89–93) requires the unmodified frozen battery's PASS. Per the assignment's authoritative observation, frozen C1 fails because E12/E13 fixtures mismatch; `c1-battery-supplement.py` is a distinct post-freeze supplement, not repair of frozen success. Candidate `ref-preflight-v3.py` is not production. No claim counter was run and no independent C1/C2/C3 closure is asserted.

## Evidence method and remaining unknowns

Evidence is direct targeted `grep` and ranged `read` of the paths above; no executable probe was required by this recon item, so command/output/exit receipts are not applicable. The initial fleet-wide filename glob timed out; narrowed package/register discovery succeeded. No `lsp` device is mounted in the current `xd://` inventory; no exported code contract was investigated and text results are documentary evidence, not semantic symbol proof.

Unresolved: current-origin quote truth; exhaustive held/staged ID collision list; full package-to-campaign row mapping. None is silently claimed. No scratch or clone was created, so none remains to delete.

## Self-evaluation

Accuracy 4/5: source locations and namespace examples are explicit; no live-source truth established. Completeness 4/5: all 24 rows covered; exhaustive collision analysis is explicitly outside this slice finding. Clarity 4/5: three namespaces separated; source paths are necessarily long. Actionability 4/5: L1 receives a bounded slice and concrete collision without adoption authority. Conciseness 4/5: historical split retained to prevent false freshness. Overall 4.0/5. Highest-impact improvement for an authorized future adoption task: document-bound source reopening and exhaustive namespace mapping. User agreement expected because this report keeps the requested no-adoption boundary.
