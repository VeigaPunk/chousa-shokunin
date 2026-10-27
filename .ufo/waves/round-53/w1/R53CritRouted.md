# R53CritRouted — round-52 closure routed defects, per-item attack (seat R53CritRouted)

Scope: `corpus/lessons/round-52-verifier-spotcheck.md` §6 items 1–6. What the round does vs the closure's words, and the cheapest way each item could look done without being done. Evidence is commands I ran or files I opened; wave seats R53DraftCorrections/R53ExecPointerAnchor/R53ExecCjkPolarity/R53DraftQuality were in-flight at review time (their assignments read from their transcripts), so item verdicts note what must land on integration.

## Grounding commands (all run by me)

```
$ grep -n 'E1–E4' corpus/lessons/round-52.md SCORECARD.md LOG.md
corpus/lessons/round-52.md:153:`corpus/evidence/round52/claims-erratum.md` E1–E4: …
SCORECARD.md:2664:… post-freeze disclosures `corpus/evidence/round52/claims-erratum.md` E1–E4. …
$ head -44 corpus/evidence/round52/claims-erratum.md   # E1–E6 bullets present (E5 in-round narrowing; E6 unbounded span-builder reader)
$ python3 - <<'PY'   # S130 raw decode
raw=open("/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/bdff491a75c6abeda1d9c01d.raw","rb").read()
t=raw.decode("utf-16le", errors="replace"); print(len(raw), len(t), t.count("是否检索灰色文献"))
PY
243929 121964 1
$ grep -E '^\| S133 |^\| S111 ' /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md | cut -c1-320
| S111 | … — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 | …
| S133 | … — https://www.medsci.cn/guideline/show_article.do?id=23e481c0052069d3 | …
$ TMPDIR=/fast/scratch/hyaku/chousa-r53/R53CritRouted python3 corpus/evidence/round53/c1-count.py --seed 7 | tail -3
LEGS=8/8
C1=PASS
exit=0        # REAL line inside: CITED=6 APPEND=5 HELD=0 TWIN=1
$ git show 5b550133d79bc09c82d8965cce2e48c2598b8c3e:tools/assimilate-rows.py | grep -n 'held\|twin\|HELD\|TWIN'
425:  held: dict[str,str] = {}         438:  mapping[sid] = (by_url[u], "held")   507:  print(f"CITED=… APPEND=… HELD={len(cited)-len(rows)}")
$ git diff --stat 5b55013 32aab5e -- tools/assimilate-rows.py    # 102+/35-; v4 adds twin/held split, TWIN count, noentry/order
```

## Item 1 — stale erratum range (E1–E4 → E1–E6)

Round does: R53DraftCorrections greps all three files, reads the erratum's real range, drafts one append-only `correction:` line per place in the R51 pointer-correction form; old lines untouched. Verifies the two stale sites exist (round-52.md:153, SCORECARD.md:2664 — my grep confirms exactly those two; LOG.md has none).

Meets closure words if, on integration: both places get a line, each line **names E5–E6** (their content: in-round narrowing; unbounded span-builder reader), not merely "E1–E6"; no old line edited.

Cheapest look-done: (a) correct only the lesson, leaving SCORECARD:2664 stale (spot-check reads the scorecard); (b) a line saying "erratum carries E1–E6" without naming E5/E6 — satisfies a grep for "E5" but voids "naming E5–E6"; (c) an ` anchor:` whose text occurs once in the target but is unrelated to the range (e.g. `"claims-erratum.md"`) — passes the new anchored check while the statement stays wrong; (d) lines appended in the report but dropped by the L1 (the pointer-anchor-check covers only SCORECARD.md and corpus/README.md, so a lesson correction is never machine-checked).

**Verdict: meet (planned), contingent on both sites, E5/E6 named, and a content-true anchor; the anchor mechanism checks presence, not truth.**

## Item 2 — grey-literature r40 refusal reason

Round does: R53DraftCorrections drafts the corrected reason sentence ("S133 duplicates the S111 URL; outside the frozen by-document set"; headline is a search-record field, in province) for the round-53 lesson and verifies the closure's decode evidence. I independently confirm both facts: decode count 1, and staged S133 = lane S111 URL (medsci show_article.do?id=23e481c0052069d3).

Meets closure words: restatement half yes (planned). The precondition half — "define a text form for OLE `.doc` captures" and "decide the regulator field record on its own source, with currency kept as an Unknown" — is assigned to no wave seat; the round's five-document set (S117–S121) does not restage S130, so the re-stage precondition stays dormant, but the field-record decision was not scheduled either. If the round-53 Gate anywhere keeps using the old province-headline rationale as decisive, item 2 is half-closed.

Cheapest look-done: the sentence lands in the lesson while the Gate still reasons from the old ground; or the verification count is done on the `.txt` sidecar instead of the UTF-16LE decode; or the restatement is placed where it cannot supersede (wrong section, not append-only). The seat is instructed to decode the `.raw` correctly, so the cheap path to watch is placement and the Gate's operative reason.

**Verdict: partially met; restatement matches the closure's words, OLE-form/field-record decision not yet scheduled (no re-stage).**

## Item 3 — representation variance in the next frozen C1-style counter: **substitution**

Claims.md says the round meets (3): "representation variance belongs in the FROZEN counter — C1's generator randomises registry-row indentation (0–3 spaces), the heading separator (space or tab), the URL scheme, a trailing `/` and the host case, all inside the census URL identity". Code confirms: `Gen.spell` (c1-count.py:96-105) varies scheme/trailing slash/host case; `registry` (126-148) varies indentation/separator.

The closure item 3 is about the **capture-text** conformance counter (round-52 C1, `tools/capture-text.py`): the enumerated dimensions — a non-`w:` namespace prefix, single-quoted attributes, CDATA, comments, non-self-closing `w:tab`/`w:br` — separate the landed tool (9/9) from the forge (5/9) on the closure's probe. Round-53 C1 is the **adopter** (`tools/assimilate-rows.py`), whose inputs are plain-text registry/staged rows: the enumerated XML dimensions cannot be expressed in them, and no round-53 counter touches capture-text (grep of round53 `*.py`: no `capture-text`, `CDATA`, namespace handling). The known forge (`controls/forge-shape.py`, 9/9 on the r52 frozen counter) therefore remains unmeasured by any frozen leg this round.

So folding identity-preserving textual variance into the adopter counter is **not** a meeting of item 3: it is a substitution — variance of a different kind, on a different tool, that does not close the routed conformance gap. The frozen adopter counter could be perfectly sound and item 3 would remain open.

Cheapest look-done: QUALITY criterion 91 (R53DraftQuality's draft) declaring defect 3 closed with "check: c1-count.py `Gen.spell`/`registry`" and a red-before quoting the r52 forge 9/9. The red-before documents the old gap; the check cannot fail on XML spelling (no XML in adopter inputs), so it is a QUALITY criterion with no check that can fail for the routed defect. Correct closure would freeze a capture-text-style counter whose generator re-spells main-part XML (namespace prefix incl. default-ns `w:`, single quotes, CDATA, comments, non-self-closing breaks) — i.e. promote the E1 supplement's generator into the frozen counter — or explicitly carry item 3 forward instead of claiming closure.

**Verdict: substitution; item 3 not met this round (open).**

## Item 4 — adopter twin-id `held` label + refusal ordering (4a); anchored `correction:` check (4b)

4a. Closure words: twin-id `held` label and refusal ordering ("routed 2"). Frozen C1 encodes exactly that: `held` only when a Registry row carries the URL, `twin` when an earlier same-run staged row minted it (same lane id, nothing appended), HELD=/TWIN= counts, recheck validated for held/twin before writing, registry refusals printed before entry refusals, refused also without `--entry`, sound registry without `--entry` exits 0. I verified v4's main flow: `refused` is seeded with registry problems first (assimilate-rows.py:440) and printed before entry refusals; `reg_bad` refuses without `--entry` (425-431); recheck refusals fire before any write (502-519; prior outputs unlinked at 432-435); held/twin split at 475-493; `HELD=… TWIN=…` printed (574). Base (5b55013) labelled every non-append row `held` and printed only `HELD=len(cited)-len(rows)`, no TWIN count — the exact routed confusion. Counter observed: `LEGS=8/8 C1=PASS` (--seed 7), REAL `HELD=0 TWIN=1`, and the controls discriminate: RELABEL (cheapest partial patch: same-run label + TWIN count only) scores 5/8 — RECHECK, ORDER, NOENTRY fail; ALLTWIN 2/8. The counter kills the obvious fakes.

Cheapest look-done for 4a: correct counts but wrong labels (killed by full map equality in every mapped leg); labels right but recheck skipped on held/twin (killed by RECHECK); registry refusals emitted after entry refusals (killed by ORDER). No look-done path found in the frozen counter; the residual is only that a twin row's "nothing appended" is verified via map equality, which the legs do compare.

4b. Closure words: anchored `correction:` check (routed 4). Round does: claims.md routes it outside the claims as ordinary work; R53ExecPointerAnchor builds `pointer-anchor-check.py` (SCORECARD.md + corpus/README.md; ` anchor: "<text>"` ≥12 chars, exactly-once in the target; later line supersedes earlier for the same <file>:<line> <ptr>; ANCHORED=a/n UNANCHORED=u BAD=b; exit 1 when a<n), red-before on the lane, drafts anchored successor lines, green-after on a scratch copy, forged/too-short anchors fail.

Meets closure words if the script lands and the anchored lines land with content-true anchors. Cheapest look-done: the script is committed but nothing runs it — criteria 91–94 (R53DraftQuality) do not reference it, so it is enforce-able only if the L1 or a Gate invokes it; or an anchor passes because it occurs once in the path yet is unrelated to the correction (presence ≠ truth); or the L1 appends the lines without anchors (red stays red, which is at least visible). Note the check's file scope misses lesson corrections (item 1).

**Verdict: 4a met (frozen claim; counter discriminates; candidate hits target). 4b planned with an enforcement gap (nothing wired to run it) and a presence-not-truth residue.**

## Item 5 — inference-ground CJK polarity fixture

Closure words: "Add a red-before fixture on a negated CJK bullet." R53ExecCjkPolarity builds a minimal lane-shaped root whose bullet quotes a CJK phrase that occurs in the capture but negates it (不要求/没有/未要求 fixtures + positive control), shows red-before (tool exits 0 on the negated bullet), writes the smallest patch to a scratch tool copy, shows green-after, and re-runs the lane's existing r50–r52 entries; diff + fixtures (corpus/fixtures/inference-ground-cjk/) go in the report. That matches the closure's words.

Cheapest look-done: the fixture is added but never run by any check (decorative; the inert leg stays inert); or the negated fixture's quoted phrase does not actually occur in the capture, so the unpatched tool already flags it for absence — then the "red-before → green-after" story is hollow (this is the "a CJK fixture the unpatched tool also flags" trap); or the patch's negator window overmatches and rewrites the entries the seat claims still pass; or the L1 lands either the fixture or the patch without the other. The fix must flow through the inference-ground leg the C2 claim runs (`tools/inference-ground.py` exit 0).

**Verdict: meet (planned); fixture must be wired into a runnable check and its positive control must locate the phrase, else item 5 stays decorative.**

## Item 6 — status-neutral p.out/p.err / relative redirects

Closure: both incidents were disclosed, moved, never committed. Round handling: seat specs + host guard mandate absolute scratch under `/fast/scratch/hyaku/chousa-r53/<seat>/` and `TMPDIR` there; no relative redirects; nothing writes fleet-root tracks. That prevents the mechanism but no check audits it; a violating W1 seat would still be caught only by the closure spot-check. Verdict: no routed action needed; unmeasured hygiene.

## Bottom line

C1 (adopter) is a genuine implementation of item 4a with discriminating controls; items 1, 2, 5 are assigned with the right shape but their closure depends on L1 integration and on checks that actually run (code 6 is harness hygiene). Item 3 is **substituted**, not met: the round freezes identity-preserving *textual* variance in an adopter counter while the routed XML-spelling forge of the capture-text counter has no frozen counter this round — and QUALITY criterion 91 is the cheapest way that substitution could look closed (a check that cannot fail on the routed defect). Smallest safe correction: freeze a capture-text-style counter whose generator re-spells main-part XML (non-`w:` prefixes, single quotes, CDATA, comments, non-self-closing breaks), or carry item 3 forward unclosed.

VERDICT: Attacked the round's handling of round-52 closure items 1–6 — item 3 is a substitution (adopter textual variance ≠ capture-text XML-spelling variance) and stays open; items 4a (frozen C1, LEGS=8/8) is genuinely met, 1/2/4b/5 meet the closure's words only if the L1 lands and wires them, with the anchor/QUALITY-criterion presence-not-truth traps named.
