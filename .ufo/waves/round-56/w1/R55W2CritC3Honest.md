# R55W2CritC3Honest — C3 honest-calibration attack

Scope: attacked the frozen round-55 C3 claim, not its predicate/target/counter/control. Axis: calibration; operability only insofar as the counter’s observation provenance is claimed. I read frozen claims at `corpus/evidence/round55/claims.md:145-191`, the BASE revision named there (`dba605deb5cd5ed4874e0e3c39ba24737409cd80`), W1 independent observations, SCORECARD errata and round-54 closure/W2 reports. No production changes.

## (a) Eleven statements vs repo state

The frozen claim enumerates targets/keys/measurements at `claims.md:159-180`. BASE statements are in the targets quoted by the appended SCORECARD lines (`SCORECARD.md:2784-2794`); each line’s observation is corroborated as follows:

| Item | Baseline mismatch and evidence | Assessment |
|---|---|---|
| E01 | R36 “belongs to no line here”; cached S122 has `该标准暂无全文，请等待更新` once at char 1712 (W1 R36 observation lines 3, 13, 25-31; closure §6.4 line 131). | Real mismatch only under broad “line” wording; latent i18n template, not displayed page. Narrow scope needed. |
| E02 | Stated phrase offset 575 vs phrase start 569. W1 R36 lines 3, 14, 25-31. | Real six-character offset error; 575 is value offset, not phrase-start. |
| E03 | “standard prescribes” taxonomy: terms `附录` and `文献类型` each zero in S121/S122 forms; W1 R36 lines 3, 15, 25-31. | Real source-support mismatch for the claim as grounded in these captures, not proof standard lacks taxonomy. |
| E04 | “count 1 each” contradicted by `国家标准委=2,2`; W1 R36 lines 3,16,25-31. | Real overbroad count statement; qualifier later clarifies scope to anchor quotes. |
| E05 | Six S101 positions independently located as 11972,12007,12795,12963,14049,25123, versus listed anchors 11170,11205,11993,12161,13247,34374; drift +802 five times and -9251 once. W1 Q97 lines 32-43; erratum line SCORECARD 2788. | Real mismatch (including transposed displayed pairs / stale anchors). |
| E06 | UTF-16LE C0 counts: 18451; excluding tab/LF 18431; excluding tab/LF/CR 18242. W1 Q97 lines 19-30. | Real count discrepancy under the counter’s multiple exclusion sets; 18242 is only one convention. |
| E07 | Defined form has U+FFFD=0 but C0=469 and LF=469, not zero controls. W1 Q97 lines 19-30. | Real mismatch: “control” count includes linefeeds; wording clarified by observation. |
| E08 | Removing both dumps yields `ANCHORED=7/16 UNANCHORED=9 BAD=9`, not BAD=6. W1 Probe lines 7, 14, 19; closure §6 item 6 line 133. | Real stale number. |
| E09 | ctypes `system()` marker SPAWNED, rc=0 under hook, contradicts “refuses delegate.” W2 CritC1Verdict lines 30-36, 69-85; SCORECARD 2792. | Real and independently probe-backed mismatch; audit-hook event coverage is incomplete. |
| E10 | Committed SHELL control says `LEGS=1/6`, not “same” as adjacent claim. W1 Probe lines 9,15,19; erratum line 2793. | Real repository-receipt mismatch, but not an independent runtime observation. |
| E11 | No-open oracle-echo returns SUPPLEMENT_LEGS=3/3. W2 SentFinal (see closure §6 item 2 line 128) and W1 report’s stated unmeasured limitation (Probe lines 10,19). | Mismatch supported by W2 observation/closure, but W1 Probe did not itself run it; cannot describe that W1 seat as independent reproduction. |

Thus all eleven are genuine contradictions between baseline self-statements and the stated observations, though their strength/provenance is not uniform: E01/E03 are scope/source-support nuance; E10 is receipt comparison; E11 is W2 evidence rather than W1’s independent run. This is not evidence that every erratum author personally observed every fact.

## (b) Copying W2 without observing

Yes, a seat can satisfy the writing side by copying the exact strings; the frozen predicate checks anchored errata against the counter’s computed committed-byte/probe observations, not authorship or epistemic process (`claims.md:147-157,182-190`). Consequently copied text cannot pass if it differs from current counter output, but matching transcription can pass without the seat independently deriving it. This measures correction fidelity, not independent discernment.

W1’s actual independent coverage: E01–E04 were independently measured with outputs `1 @1712`, `569`, term counts `0,0`, and `2,2` (R55ExecC3ObsR36.md:7-21); E05–E07 independently measured, including all six positions, count conventions and form counts (R55ExecC3ObsQ97.md:19-43). The W1 SCORECARD verdict explicitly claims independent matches only for E01–E07 (SCORECARD.md:2806). W1 Probe says E08 and E10 observed, E09 probe failed syntax before hook and E11 execution was not run (R55ExecC3ObsProbe.md:7-19); hence no independent W1 confirmation for E09/E11. W2 reports / frozen counter can support their exact observations, but copying their numbers is not independent observation. That does not invalidate the frozen predicate; it limits the calibration interpretation and any claim of all-eleven independent derivations.

## (c) W2 falsifications not represented as errata

Closure `corpus/lessons/round-54-verifier-spotcheck.md:126-134` is the compact W2 census. C3’s eleven items cover C1 forge/delegate and calibration defects, but not the distinct observations in closure §6 items 1-3 and 7:

- Item 1: uncommitted W2 output/reports (integration/provenance issue).
- Item 2: REAL leg echoes inherited TMPDIR; forge builder leaves pinned captures on SIGKILL; ledger checker escapes root; PDF cross-check passes vacuously. These are distinct from the C3 E09 delegate and E11 oracle-echo claims, and lack C3 errata.
- Item 3: RW-1 recurrence, frozen counter and supplement forgeability as a recurring weakness (not itself a self-statement among E01–E11).
- Item 7: five carried W04 duplicate-URL warnings S051/S053/S073/S074/S075 (not a self-statement among E01–E11).

Other W2 findings in `R54W2CritEntailSta.md` and `R54W2CritMistakes.md` map to E01–E08 (with E03/E04 nuance); E10 maps to the SHELL receipt. The five W04 warnings and the distinct closure §6 item-2 defects are real omissions from the eleven errata set, but they are not omissions from the frozen C3 predicate: it enumerates only eleven specified self-statements. Route/disposition them elsewhere; do not add/change frozen C3 items.

## Axes and smallest safe correction

- **Calibration:** C3’s 11/11 counter result is not inflated on factual mismatch count: each observation contradicts its keyed BASE assertion. But it must not be read as 11 independently observed author corrections; only E01–E07 have W1 independent re-derivation, E08/E10 partial W1 evidence, E09/E11 rely on other evidence/counter.
- **Operability:** counter-computed comparison constrains copied strings to match observed output, but does not establish the seat’s process. E09 hook bypass is a separate recorded limitation, not a reason to rewrite frozen requirements.
- **Depth:** closure omissions are outside C3’s fixed eleven targets and require separate disposition.

Smallest safe correction: retain the frozen predicate/results; describe C3 as counter-checked correction fidelity for eleven mismatches, qualify independent W1 derivation as E01–E07 only (plus E08/E10 receipt/probe evidence), and separately route closure §6 items 1-3 and 7 rather than implying E01–E11 exhaust W2 findings.

VERDICT: C3 is an honest but bounded calibration move; all E01–E11 are genuine mismatches, while W1 independent derivation is incomplete (E09/E11) and distinct W2 defects remain outside its errata scope (closure §6 items 1-3, 7).