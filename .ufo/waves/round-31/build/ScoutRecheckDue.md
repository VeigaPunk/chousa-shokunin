# ScoutRecheckDue — SOURCES.md rows due for recheck (round 31)

Date: 2026-10-23. Assigned: parse `corpus/SOURCES.md`; find rows whose `recheck`
cell is a date on/before 2026-10-23 or a condition round 31 triggers; report id,
source host, host registration, status. Nothing fetched.

## Method (all local, read-only)
- Parsed the Registry table of `corpus/SOURCES.md` (56 data rows, S001–S056)
  with a Python table parser (unescaped-pipe cell split); extracted id, source
  URL host, kind, status, opened, recheck per row.
- Recheck grammar per QUALITY 6 / round-26 decision table (`recheck-due-r26.md`):
  ISO date | `Nd` cadence (due = opened + N calendar days, proleptic Gregorian) |
  `on-release` (event, no calendar deadline) | unknown/absent.
- As-of date 2026-10-23.

## Findings

### 1. No row is due by date or cadence
Recheck cell distribution: 26× `365d`, 23× `on-release`, 4× `90d`, 3× `180d`.
Zero literal ISO dates; zero absent/unknown/malformed. Earliest cadence deadline:
S006/S007/S015 (opened 2026-10-19, `90d`) → due 2027-01-17 > as-of. So no row
meets "date on or before 2026-10-23".

### 2. Condition rows: all 23 `on-release`
Round 31 is a gate release: both frozen claims edit `tools/research-gate.sh
verify-claims` (base gate sha `ac1315ddaa12e79b68069d1a9866b9b1b55e3a43efef3ba0cb5ca5e665835765`).
Split by what the release event tracks:

**Triggered by round 31 (own-work rows whose source IS the gate/lane artifacts) — 9:**
| id | host | registered? | status | kind |
|---|---|---|---|---|
| S001 | local (chousa research gate) | n/a (own-work) | mined | own-work |
| S034 | local (round-26 measurement log / gate) | n/a | mined | own-work |
| S035 | local (round-26 claims / gate) | n/a | mined | own-work |
| S036 | local (round-26 claims / gate) | n/a | mined | own-work |
| S040 | local (.ufo falsify report) | n/a | mined | own-work |
| S041 | local (.ufo falsify reports) | n/a | mined | own-work |
| S042 | local (.ufo falsify reports) | n/a | mined | own-work |
| S043 | local (.ufo falsify reports) | n/a | mined | own-work |
| S045 | local (.ufo residual report) | n/a | mined | own-work |

**`on-release` but NOT triggered by round 31 (event tracks the external host's release) — 14:**
| id | host | registered? | status | kind |
|---|---|---|---|---|
| S004 | www.cochrane.org | no | mined | docs |
| S008 | www.cochrane.org | no | queued | docs |
| S017 | www.prisma-statement.org | no | queued | spec |
| S019 | www.cochrane.org | no | queued | docs |
| S025 | www.rfc-editor.org | yes | rejected | spec |
| S029 | www.cochrane.org | no | mined | docs |
| S038 | docs.python.org | yes | mined | docs |
| S044 | docs.python.org | yes | mined | docs |
| S049 | docs.python.org | yes | mined | docs |
| S052 | docs.python.org | yes | mined | docs |
| S053 | docs.python.org | yes | mined | docs |
| S054 | docs.python.org | yes | mined | docs |
| S055 | docs.python.org | yes | mined | docs |
| S056 | docs.python.org | yes | mined | docs |

[INFERENCE] "on-release" on external-host rows means that host's release (cf.
`contextual-source-admission-r24.md` recheck note "on-release (S004, Cochrane
Handbook — v6.5 … as read)"), i.e. a Cochrane/PRISMA/RFC/Python-docs release;
round 31 releases none of those, so none of the 14 is triggered by this round.

### 3. Registered hosts
Registered fetch hosts in the registry: www.rfc-editor.org, www.w3.org,
docs.python.org. Among all `on-release` rows only docs.python.org (S038, S044,
S049, S052–S056) and www.rfc-editor.org (S025) are registered; no W3C row is on
`on-release`. Hosts not in the registered set and not local: www.cochrane.org,
www.prisma-statement.org.

## Verdict orientation (L1 decides which to re-open)
- Due by round 31 (gate release): the 9 own-work rows S001, S034, S035, S036,
  S040, S041, S042, S043, S045 — gate behavior changed by both C1 and C2, so
  gate-behavior claims need a re-open to keep their anchors honest.
- The 14 external-host `on-release` rows are event-due only for their own hosts'
  releases; round 31 does not trigger them. No dated/cadence row is due.
