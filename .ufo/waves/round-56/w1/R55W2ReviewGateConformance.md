# R55W2ReviewGateConformance — section 10 and W04

Target: round-55 landed state `29cfb12abd70f688b48c0d17f31e636f2d81104a`; frozen-claim context read from `corpus/evidence/round55/claims.md`. Compared `corpus/lessons/round-55.md` `## Gate` with fleet prompt `chousa-round-55.md` §6 item 10. No changes made to lane production files.

## Gate conformance

- Collision evidence: Gate states registry 123 IDs (S001–S123), staged 114, collision count 42 (S082–S123), quarantine slice 24; it records the scratch guard proof and renumbering by URL/document (staged S130→S124, S131→S125, S143→S126; staged S133 matches held S113 and is not cited). At pinned commit, `.ufo/waves/round-55/assimilation/` contains `reg-ids`, `staged-ids`, `collisions`, `quarantine-slice`, and guard proof files. `git show 29cfb12...:.ufo/waves/round-55/assimilation/collisions | wc -l` → `42`; quarantine slice → `24`. Guard receipt says two-space `| S002 |` is caught by c03 and not column-zero c0. Thus counts and evidence are present; the lesson itself summarizes lists by count/range rather than pasting all 123/114 IDs inline. The prompt specifically directs both lists into the report; the Gate points to committed lists, so this is an evidence-location/presentation gap, not absence of collision work.
- Recheck normalization: Gate explicitly records stripped staged prose for S130/S131/S143 and says rows retain `180d`; this meets the requirement to preserve removed prose in the Gate. It identifies the superseded UTF-16 decode assumption and the replacement `capture-text.py --locate` recheck.
- Admission/rejection: both explicit. Entry `grey-literature-and-chinese-search-record-r40.md` admitted narrowed; `grey-literature-field-boundary-r43.md` refused with reason and flip condition. A `refused-doc` URL line is present for the Guizhou S161 document. Re-opened-source table gives access date, defined forms and located quotes.
- Quarantine: Gate says the slice has 24 rows, and identifies the one theme URL row as register S125 round6, then gives a verdict and evidence distinguishing its absent-as-written third quote from two present quotes. This satisfies the assignment's theme-row check. Important scope note: §6 item 10's special wave-4 rule says the lane's *first* assimilation round must hand-check all 24 rows and adopt nothing. Round 54 prompt also contains the assimilation contract (fleet prompt search returned the contract and wave-4 quarantine-first text), so round 55 is not the first round under the item; the first-round restriction does not invalidate this adoption. No basis here to demand 24 new verdicts in round 55.

## W04 adjudication (pinned `corpus/SOURCES.md` rows)

- S050/S051: same dated HTML 5.2 URL, distinct anchors and documented scopes (optional end tags vs in-head insertion mode). Keeping both is justified.
- S052/S053: same Python socket page, distinct anchors/scopes (timeout mode vs `create_connection`). Keeping both is justified.
- S059/S074: same hashlib page/scope; S074 explicitly rejected as duplicate of S059. Correct disposition.
- S070/S073: same coreutils sha256sum source and scope; S073 corrects S070's anchor label and explicitly supersedes it. S070 remains mined and cited by two entries; retaining it alongside the correction is justified, with the correction clearly recorded.
- S071/S075: the rows identify different coreutils tools and distinct scopes (`env -u` vs `mktemp -d`); they do not constitute a duplicate-scope pair despite shared manual URL. Keeping both is justified.
- S072: among the specifically requested rows, S072 is not part of a W04 pair in the Gate's list; its bash exported-function scope is distinct and no duplicate disposition is asserted.

Evidence: extracted pinned files with `git -C /home/vgpnk/Projects/shokunin/chousa-shokunin show 29cfb12abd70f688b48c0d17f31e636f2d81104a:corpus/lessons/round-55.md` and corresponding `corpus/SOURCES.md`; source rows S050–S053, S059, S070–S075 are at pinned SOURCES lines 60–85. The prompt text was read at §6 item 10 (lines 496–593); round-54 prompt search found the same assimilation and quarantine-first directive.

VERDICT: Round-55 Gate substantially conforms and its W04 pair dispositions are right; collision lists are committed as evidence but are summarized, not pasted inline in the Gate.