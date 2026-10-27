# R55ScoutW04 — W04 duplicate-URL adjudication

## Evidence

Read `corpus/SOURCES.md` rows S051, S053, S073, S074, S075 and twins S050, S052, S070, S059; paths and scopes are quoted from those rows. Ran:

```sh
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin chousa
```

Observed (exit 0):

```text
chousa W04 S051 duplicate url www.w3.org/TR/2017/REC-html52-20171214/syntax.html across scopes
chousa W04 S053 duplicate url docs.python.org/3/library/socket.html across scopes
chousa W04 S073 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa W04 S074 duplicate url docs.python.org/3/library/hashlib.html across scopes
chousa W04 S075 duplicate url www.gnu.org/software/coreutils/manual/coreutils.html across scopes
chousa ok /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

`CORPUS.md` lines 116–118 defines append-only registry treatment: only status/recheck/used-by change in place; correction is a new row whose teaches begins `supersedes S0NN —`. W04 is defined in `scripts/sources-census.sh` lines 31–33 as same URL across scopes; it is a warning, not validation failure. W04 specifically means URLs normalized by the census to host/path; fragments do not disambiguate URL identity.

## Pair dispositions

1. **S050/S051 — legitimate distinct scopes; retain both.** Both rows point to the same dated HTML 5.2 syntax page but different fragments/sections: S050's optional-tags rule on omitting `</head>`; S051's in-head insertion-mode tree-construction boundary. These answer separate source claims (extractor's head-end-tag assumption vs token handling once in head), and S051 explicitly limits its scope to the head boundary, not fetch behavior or quote verification. No superseding row warranted. Lesson: a shared page URL is not automatically a duplicate when the cited clauses and resulting claims are distinct; record fragment/section and narrow scope.

2. **S052/S053 — legitimate distinct scopes; retain both.** Same Python socket documentation page, distinct fragments: timeout-mode semantics versus `socket.create_connection` host resolution/address attempts. One supports per-operation timeout vs elapsed deadline; the other supports DNS/address connection behavior. Explicit scopes in both rows exclude the other's proposition. Lesson: assess the claimed API behavior and section, not just page URL; a URL-level warning can be valid multi-scope sourcing.

3. **S070/S073 — duplicate source/scope; S073 is the already-appended correction, S070 should be superseded.** Both concern the installed `sha256sum` digest text and `--check` semantics. S073 states `supersedes S070` and corrects the erroneous anchor label while retaining the quote/offset. Under append-only rule 2, do not rewrite/delete S070; flip its status to `rejected` (record old→new in the lesson), and leave S073 mined. That disposition makes the correction authoritative without a stale duplicate remaining active. The current validator does not warn this pair because its S073 teaches includes the literal `supersedes S070` marker.

   **Proposed append-only flip:** `S070 status: mined → rejected` (log the old→new change in round lesson); no new row needed because S073 already supplies the correction.

4. **S059/S074 — duplicate proposal correctly rejected; no further flip.** Same Python `hashlib` URL and digest-input scope. S074 is already `rejected`, explicitly says S059 holds this page/scope, and provides a distinct-scope flip condition. Keep both rows; do not supersede S074 or change status. Lesson: retaining a rejected duplicate proposal is useful curation evidence, not an admitted duplicate; its flip condition must name a genuinely unstated property.

5. **S071/S075 — legitimate distinct scopes; retain both.** Same GNU coreutils manual URL, but S071 is `env -u` environment scrubbing, while S075 is `mktemp -d` safe directory creation. Distinct manual pages/anchors and unrelated documented contracts. Lesson: coreutils' shared manual landing URL does not imply shared source scope; preserve the command-specific anchor and scope.

## Lesson text proposed for round-55 integration

```text
### W04 duplicate-URL adjudication
The source census emitted five W04 warnings (S051, S053, S073, S074, S075). W04 compares URL across scopes; it is a warning, not an error. Keep S050/S051 (HTML 5.2 optional tags vs in-head tree construction), S052/S053 (socket timeout semantics vs create_connection resolution), and S071/S075 (env -u vs mktemp -d): each pair has distinct sections and teaches distinct, narrowly scoped claims. S074 remains a rejected duplicate proposal for S059's hashlib scope. S073 already corrects S070's sha256sum anchor and explicitly supersedes it; apply only the permitted append-only status flip S070 mined→rejected and log that change old→new. Do not collapse distinct scopes merely to silence W04; use a superseding row when correcting an admitted row, and retain rejected proposals as rejection evidence.
```

## Verdict
VERDICT: adjudicated all five carried W04 warnings: three legitimate shared-page multi-scope pairs, one already-rejected duplicate proposal, and one correction requiring the append-only S070 status flip to rejected.