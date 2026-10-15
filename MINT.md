# MINT — chousa-shokunin (2026-10-14)

**Cause:** operator directive (the 12-hour shokunin fleet program, 2026-10-14),
plus an unowned domain the roster could not absorb.

**Demand instances (evidence):**

1. **`~/Projects/shokunin/research/` holds a deep-research pattern with no owning
   lane.** Three artifacts exist at `research/deep-research-2026-09-28/`
   (`A-shokunin-tradition.md`, `B-multiagent-knowledge.md`,
   `C-rank-taxonomy.md`) produced by an operator research pass. They are
   archived, unindexed, and no lane's province claims the METHOD that produced
   them. Evidence: the files plus `research/README.md`.
2. **kasegi does program-specific bounty research only.** Its province is bounty
   and security programs, program rules and claim packages
   (`kasegi-shokunin/PROVINCE.md`) — it explicitly refuses general source
   research. The general method (question framing, source hierarchy, citation
   chaining, claim verification) is therefore unowned.

**Roster scan (rejected fit):** 17 lanes scanned
(`.ufo/scopes/shokunin-12h-20261014/mint-roster-scan.json`). kasegi —
bounty-scoped, refuses general research. kengaku — model evaluation, refuses
general source research. kumitate — orchestration, refuses. lore — fictional
canon, not factual research method. No province absorbs the research method.

**Domain boundary:** the method only. Refuses external live-target research
without operator approval, bounty-program scope (kasegi), and model-quality
claims (kengaku).

**Probation:** >=3 verified rounds before a roster row. Roster row withheld.

## Integration guard (appended 2026-10-15, before corpus land)

Round 1's critic measured a trap the corpus landing must not walk into. Recorded
here because the risk is in the *index*, not the method notes:

- **Do not copy `research/README.md:10-14` into this corpus.** It would treat
  `jin'i-ryu` as a verified coined rank. Export A only says the spelling was **not
  substantiated** and should be treated as coined
  (`research/deep-research-2026-09-28/A-shokunin-tradition.md:64`); export C adds
  that `jiritsu-ryū` is not a verified translation
  (`C-rank-taxonomy.md:109,124`). The live token is already operational at
  `PROTOCOL.md:21`. Copying the gloss would be false provenance, a duplicate
  authority, and a mint-boundary breach (`MINT.md` domain boundary above).
- **Keep only the method specimens, tagged `export-unverified`.** Do not quote the
  ACE numerals (`B-multiagent-knowledge.md:79`) without their case-study hedge —
  that launders a model-quality claim into method, which is kengaku's province.
- **Do not relabel `jin'i-ryu`, and do not add four- or five-axis rank lists.**
- Items asked in the export prompts (A(2)–(4), B(2)–(3), C's rank-inflation
  catalog) appear **only in the prompt lines** — the answers were never given. Do
  not invent them.
- Rejected recipients for this material: lore, kotoba, kasegi, kama, kumitate,
  tameshi. Lexical and workshop rows stay unowned.

### Provenance guard (appended 2026-10-15, measured)

`research/README.md:6-8` asserts provenance the dumps do **not** carry: burner Chrome,
CDP 9222, "fired by L0", "no Deep Research entitlement", and "9/8/10 searches". The
visible search labels in the exports are **1, 1, and 2**; C's `10 more` is a
collapsed widget (U+2068/U+2069), not a total. L0 is the operator side channel
(`MISSION.md:84-88`), not a model, and it is not the commit author. Do not cite the
README's provenance as fact.

Measured landing: commit **`0863746`** (`integrator <integrator@shokunin.local>`,
`2026-09-28T22:51:25-03:00`) is the only commit touching `research/` and adds the
README and A/B/C together; blobs unchanged at HEAD. It is an ancestor of HEAD but
not on the first-parent line, and `LOG.md`, `l0-questions.md`, and the watchdog log
covering that minute do not mention the harvest. Filesystem birth `2026-10-13` is
relaunch materialization, not production time.

**Unknown and to be recorded as unknown:** provider model id, selected effort,
conversation id, whether the live answers continued past the 5–9 KiB cuts, and which
process sat behind the integrator identity.

### Scope guard (appended 2026-10-15, from the meta-craft audit)

The survey contains **three incompatible axis lists**, not one method wearing artisan
names, and only one has already leaked into the index: `research/README.md:13-14`
lifts `A-shokunin-tradition.md:54` (competence / independence / improvement /
transmission) as "usable axes". `B-multiagent-knowledge.md:57` and
`C-rank-taxonomy.md:67` offer two other lists. **None matches
`chousa-shokunin/SKILL.md:17-21` or `AXES.md:7-16`.**

Requirements for the corpus landing:

- **One scope tag per sentence** — `general | general-narrow | non-general` — before
  any survey sentence enters `corpus/knowledge/`. The audit classifies 14 general
  method-forms (`MC-G01`–`MC-G14`) and 47 non-general rows (`MC-N01`–`MC-N47`),
  including the English rename Initiate → Grounded → Maintainer → Agentwright.
- **Do not add a second axis taxonomy.** Where a fleet gate already states a form,
  the gate is the authority, not the survey.
- **Do not amend `PROTOCOL.md:21`** (the live `jin'i-ryu` token).
- Twelve solicited questions are absent from the response bodies (`MC-X01`–`MC-X12`);
  **truncation is unknown, not a negative finding**.
- `B:77`'s observation / interpretation / established-knowledge split is not
  supported by the ACE case it cites, and already lives at `SKILL.md:48` (line numbers re-derived after the +3 shift below); `C:126` is
  unlabeled engineering opinion after a dictionary block; `A:88` is a promotion
  metaphor that `PROTOCOL.md:61-67` already forbids.

### Secrecy guard (appended 2026-10-15, from the sentinel audit)

Hard refusals for the round-2 fixture and the gate. These are work-queue items that
must not become grants:

- **Refuse `ApprovalTable` rows M-01 and M-02** (burner-profile read, CDP metadata
  read). `research/README.md:6` still names CDP 9222; the musketeer profile is absent
  and `ss` shows zero listeners there. **Never interpolate `9222` into a client.**
  Pending is not approval.
- **Never implement an "opens" verb.** `RecordShape.md:147` says a resolved hop
  *opens*; a hop resolves to a **path**, and nothing in this lane opens, fetches, or
  executes a resolved target.
- **Harden the gate's secret screen.** `ResearchGateDesign.md:331`'s `SECRET_SHAPE`
  matches only `keyword=` / `keyword:` and misses unlabeled `op://`, `sk-`, `ghp_`,
  `eyJ` and PEM blocks. It must not echo a match (keep the quiet grep) and must
  cover those forms before it can be trusted as a screen.
- **No `..` in a resolved path.** `ptr_file_resolves` treats any absolute path as
  `path-ok` after a `stat`, including `..` — resolution must reject traversal, and
  a `stat` is not a content read (do not claim one).
- **Fixture hardening:** serve the docroot only (not a whole tree), pin the client
  (no overridable `CHOUSA_CURL`), fully unset proxy vars, rename `account.json`,
  and extend the token grep to `Bearer ` / `eyJ`.
- Export chrome at lines 1–33 is **session inventory, not a credential value** —
  cite the line; do not copy the display name or the sidebar titles.

### Chaining guard (appended 2026-10-15)

**Do not inherit a fleet citation gate as the chain walker.**
`claim-ledger.sh citations` and `anchorcheck.py`, run read-only over the four survey
files, both return **clean with zero recognized cites** — their matchers do not see
bare hosts or `+N`, so either would certify a set in which every bibliographic hop is
unwalkable. chousa's gate must recognize the export citation forms (bare host,
aggregator chip, `+N` / isolated "N more", author-year search key) and fail closed on
them, or it inherits the blindness it exists to fix.

**Worked broken hop, for the note and the fixture:** `B-multiagent-knowledge.md:79`
attributes 18,282 / 122 / 66.7 / 57.1 / 63.7 to ACE; the only nearby furniture is a
six-work cluster, the host `arxiv.org`, and `+6`. A host is not a document and `+6`
does not expand to locators. Status: **unresolved, not contradicted** — the export
ends at `B:81` before any quotation. Searching arXiv to invent the paper would be a
*new search*, not the next hop. Repairing it from `B:49-51` was rejected: that chip
shares no identifier with the figures.

**Same content step, both ends on disk:** `research/README.md:12` ("jin'i-ryu is NOT
an attested artisan rank") names `A-shokunin-tradition.md`, which exists — but
`A:47`/`A:64` only say the search did not substantiate it. **The filename resolves;
the closed negative does not.** File existence is not enough: the cited span has to
be opened, and a summary or another citation is the next hop, not the terminus.
