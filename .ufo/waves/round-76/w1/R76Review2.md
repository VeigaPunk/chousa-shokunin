# R76Review2 — C2 measurement review

Frozen controls: `da9ac7ec684fe9fe9ad5554cab6180057255b76b`. Read `claims.md` first. Axes: authored-statement identity; polarity; magnitude; rendered visibility; section position; ancestry/append-only; battery discrimination. Recommendation only: preserve frozen instruments and route these defects/limits; no admission judgment.

**SURVIVORS=9** correction-fixture attempts printed `C2V=PASS checks=9/9`, each exit 0. These are not nine independent root causes: A3/A3b share a magnitude-parser gap, A1/A8 share a rendered-structure gap. Exact case text, every printed CHECK line, invocation and rc are in `R76Review2/counter-forgeries-blinded.txt`; complete fixture texts and commit histories are in `R76Review2/fixture-history.txt`.

## Findings by severity

### High — authored-bullet identity still rebinds (A5)

`corpus/evidence/round76/correction-count-v2.py:85-98` chooses the first prefix match, without uniqueness or exact identifier delimiting. Insert an additional `- Admit S182` bullet above the original containing the eleven-word quote `one two three four five six seven eight nine ten eleven` and `(13 words)`. Append:

```markdown
## Correction — round-74 quote counts

Superseded: the authored bullets now record 13 words and 13 whitespace tokens. The quoted strings carry 11 and 11 whitespace tokens.
```

Observed `DERIVED=S182:11 S183:11 RECORDED=S182:13 S183:13`, followed by all nine PASS checks and rc 0. The original authored bullets remain unchanged below the decoy and still derive 16/11 and record 18/13. V1/V2/V3 certify the wrong bullet rather than rejecting ambiguity. The battery's S999 decoy does not cover a repeated S182 prefix. This is a concrete Q136 identity gap, not merely a semantic-entailment objection.

### High — net-diff does not establish append-only history (A7)

`correction-count-v2.py:152-156` counts removals only in the endpoint diff. Within base..rev, delete `removable line` in one commit, then restore it and append GOOD_BLOCK in the next. Observed V8 `PASS removed lines=0` and total 9/9, rc 0. Preserved history shows the intermediate deletion.

This obeys the frozen counter's explicitly documented endpoint-diff rule; it is NOT evidence that its literal rule was executed incorrectly. It does show that Q136's previously identified deletion-history failure remains, and contradicts `c2-battery.py`'s description of the deletion-history control as “append-only, not net-append.” Its single case commit cannot exercise deletion followed by restoration. Do not retroactively change the frozen rule.

### Medium — hidden block body accepted (A1), fenced sample accepted (A8)

`correction-count-v2.py:101-106,134-135` checks comment state before the heading only. A1 appends:

```markdown
## Correction — round-74 quote counts

<!--
Superseded: 18 words and 13 whitespace tokens. The quoted strings carry 16 and 11 whitespace tokens.
-->
```

The heading is visible, but the entire correction body is commented out. V9 prints `PASS block inside comment=False`; all checks PASS, rc 0. A8 wraps the same heading and sentence in a fenced `markdown` code sample after `# Appendix`; all nine checks again PASS. No Markdown renderer was run; visibility descriptions follow the ordinary HTML-comment/fenced-code syntax. The frozen V9 explicitly promises only heading-comment exclusion, so A1 demonstrates its narrowness rather than a literal violation of that narrow wording. The broader comment-only class is not closed.

### Medium — wrong rendered magnitude accepted (A3, A3b)

`correction-count-v2.py:127-129` accepts only recognized magnitude matches and does not require that all stated magnitudes be recognized. Append under HEAD:

```text
Superseded: 18 words and 13 whitespace tokens. Correction: 16 and 11. The quoted strings carry **161** whitespace tokens.
```

A3 prints V5 `PASS magnitudes=18,13`; 161 is absent because closing emphasis separates digits from whitespace. All nine checks PASS, rc 0. A3b replaces the final phrase with `161 whitespace-token units`; same result. A3 is the stronger representation-boundary example; A3b is outside the parser's explicitly enumerated unit grammar. Neither is evidence that a plain `161 whitespace tokens` passes.

### Medium — negating prose accepted (A4)

`correction-count-v2.py:123-126` tests a fixed cue list. Append under HEAD:

```text
Superseded: 18 words and 13 whitespace tokens. The counts 16 and 11 are false and must be disregarded as corrected values.
```

V4 prints `PASS corrected lines=1 negating=0`; total 9/9, rc 0. The text expressly rejects the counts but uses neither `not ` nor the other six cues. This limits the claimed polarity test; frozen claims already disclaim proof of prose meaning.

### Medium — no correction append required (A6)

Put BASE_LESSON+GOOD_BLOCK in the base commit; the case commit adds just a blank line. V7 `PASS base ancestor of rev=True`, V8 `PASS removed lines=0`, total 9/9, rc 0. Thus those checks prove ancestry and endpoint nondeletion, not that the correction was absent at base or appended during the measured range. Relevant to Q119's do-nothing/base-already-at-target warning. This satisfies the frozen V7/V8 wording and must be reported as a measurement limit, not a failed ancestry implementation.

### Low — last literal h2 is narrower than last section (A2)

Append the valid block, then `# Boundaries` and additional text. V6 still prints `PASS last section='## Correction — round-74 quote counts'`; total 9/9, rc 0. `last_section_heading()` at lines 80-82 ignores h1 headings. The block is not the final document section, but it IS the final literal `## ` section, so this is a frozen-definition boundary, not a contradiction of the narrow V6 wording.

## Battery attacks and control

Commands, each from `/fast/scratch/hyaku/chousa-r76/R76Review2`:

```text
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/c2-battery.py --counter counters/constant-pass.py --work battery-work-constant-pass
  rc=1; C2_BATTERY=FAIL bogus_rejected=0/6 positive=1/1 lane=PASS
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/c2-battery.py --counter counters/constant-fail.py --work battery-work-constant-fail
  rc=1; C2_BATTERY=FAIL bogus_rejected=6/6 positive=0/1 lane=FAIL
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/c2-battery.py --counter counters/keyed.py --work battery-work-keyed
  rc=1; C2_BATTERY=FAIL bogus_rejected=5/6 positive=1/1 lane=PASS
python3 -B /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/c2-battery.py --counter /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/evidence/round76/correction-count-v2.py --work battery-work-control
  rc=0; C2_BATTERY=PASS bogus_rejected=6/6 positive=1/1 lane=PASS
```

**Neither constant counter passes. Battery-survivors among the three counterfeit counters tested: 0.** The keyed counter accepts the fixed `Round 76 fixture.` literal or the real-lane basename, but deletion-history also carries that literal and is incorrectly accepted, so the battery correctly rejects this particular cheat. Do not report it as a successful battery forgery. Full printed fixture results are preserved in `R76Review2/battery-*.txt`, along with counterfeit sources.

## Reproduction and provenance

The final probe command was `python3 -B /fast/scratch/hyaku/chousa-r76/R76Review2/drive.py`, cwd that scratch directory, rc 0. It fails closed unless every reported attempt reaches 9/9. Each subprocess command and rc is in the blinded receipt. Source saved as `R76Review2/drive.py`; re-create scratch at the declared path to replay after cleanup.

The final probe uses opaque random fixture directories, shuffled iteration, uniform `base`/`case` subjects, captured child output, and asserts fixture toplevel before add/commit. An initial exploratory run used named directories/order; its receipt is preserved as `counter-forgeries.txt` but the nine survivor conclusions above use the later opaque/shuffled receipt. Probe source is not sandboxed against same-UID inspection; no arbitrary adversarial process-isolation claim is made. Frozen counter code, not a newly invoked agent runtime, was the subprocess under test.

Live bytes matched frozen control blobs before scoring:

- counter SHA256 `610e5655af2bd2f5f034edcfc732b012db29d8a9ff7295cae8edce835982ecbb`;
- battery SHA256 `7e0d6832b705a81d48a1143d0b039dbaeec0665dc01fc8cbd977f97edc0d8619`.

No production edits, network, installs, commits in lane/fleet, or subagents. Git mutations were disposable fixture commits only. Early exploratory fixture commits preceded adding the explicit toplevel assertion; their cwd was nevertheless the fixture via `git -C`. The frozen battery itself also performs fixture commits without that assertion; it was not edited. These are process limitations, not claims of full guard compliance.

## Residual risk / verification gaps

The exact frozen C2 predicate still passed with the real counter: these new cases do not retroactively change its six named bogus fixtures. The important gap is extrapolating six fixed fixture rejections to closure of their entire classes. Frozen definitions explicitly narrow several checks; preserve those distinctions. A1/A2/A3/A3b/A4/A6/A7/A8 illustrate limits; A5 demonstrates authored-statement ambiguity concretely.

`xd://lsp` is not mounted (device returned “No such tool”), so semantic references/definition/diagnostics were unavailable. Source inspection plus real committed-input CLI runs supplied evidence, not grep-as-semantic-proof. No unrelated runtime/resume/saturation claim was in this seat's scope. No unrelated-base false acceptance was demonstrated; V7 ancestry bypass is not claimed. No actual diff patch was applied; this review concerns frozen instruments and their callers.

Self-evaluation (1–5): accuracy 4 (nine observed receipts, semantic-versus-literal limits distinguished); completeness 4 (all requested axes and constant controls covered, no Markdown rendering exercise); clarity 4 (related survivors grouped rather than nine root causes); actionability 4 (saved driver/history/receipts, frozen bytes unchanged); conciseness 4 (full raw outputs kept in attachments). Average 4.0. Improvement priority: successor controls for duplicate authored identifiers and multi-commit deletion history; user-facing interpretation must remain narrower than generic class closure.
