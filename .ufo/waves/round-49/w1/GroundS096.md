# GroundS096 — wave 1, round 49 (chousa) — re-ground staged row S087 → lane S096

Seat: GroundS096 (leaf; no subagents, no background jobs). Assignment: re-ground staged row S087
(staged id → lane id S096 per `adopt/renumber.tsv`) for C2, by document, on the on-disk capture;
draft the lane Gate block; re-check absent-defect-register row S082 against the capture.

## Sources opened (all read-only)

- `/home/vgpnk/.omp/agent/RULES.md` (tooling authorization; no install is expected — nothing was installed).
- `chousa-shokunin/corpus/evidence/round49/claims.md` (frozen C1/C2 predicates; neither touched).
- `/home/vgpnk/Projects/shokuknow/merge/chousa/knowledge/corpus/knowledge/aggregator-vs-source-r36.md` (staged entry citing S087).
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache/09fc63de41f293d43d631c46.txt` (12901 bytes) and `...09fc63de41f293d43d631c46.raw` (41404 bytes).
- `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md` (row S082).
- `chousa-shokunin/corpus/lessons/round-48.md` (Gate table, S082 verdict).
- `chousa-shokunin/.ufo/waves/round-49/assimilation/adopt/renumber.tsv` and `.../append.md` (S087→S096 mapping, row S096).

## Verification run (python3)

```
$ python3 - <<'EOF'
import hashlib
url="https://support.nii.ac.jp/ja/cir/manual_articles_detail"
print(hashlib.sha256(url.encode()).hexdigest()[:24])
EOF
09fc63de41f293d43d631c46
```
URL key matches the capture file name. `.raw` decoded as UTF-8 HTML (`<!DOCTYPE html> ... lang="ja"`), NOT UTF-16LE; the `.txt` is a clean, non-lossy text form, so the `.txt` is the quote form.

Quote location (python `text.find` on the `.txt`, all `occ=1`):

| quote | chars | ws words | offset | line | form |
|---|---|---|---|---|---|
| 実際の論文の参考文献のうち、CiNii Researchの同定・統合処理で、同定・統合された参考文献だけが表示されます。 | 60 | 2 | 3646 | 565 | .txt |
| 参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています。 | 38 | 1 | 3707 | 565 | .txt |
| CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており、（それに伴って）別の手法で同定・統合処理を行っているため 、CiNii Articlesの「参考文献」「被引用文献」の結果とも必ずしも一致していません。 | 125 | 6 | 3752 | 567 | .txt |

Slice-verify at each offset: `s[off:off+len(q)]==q` → True for all three (byte-exact copy). `※CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません。実際の論文の参考文献のうち、…` starts at offset 3598 (line 565); quote 3 starts the second 注意書き at line 567. Each quote occurs EXACTLY ONCE in the .txt.

## Gate block draft (lane S096)

- URL: https://support.nii.ac.jp/ja/cir/manual_articles_detail
- access date: 2026-10-25
- Quotes:
  - “実際の論文の参考文献のうち、CiNii Researchの同定・統合処理で、同定・統合された参考文献だけが表示されます。” (.txt char 3646)
  - “参考文献数も、論文での掲載数ではなく同定・統合された分をカウントしています。” (.txt char 3707)
  - “CiNii Researchでは、CiNii Articlesとは 文献の収録範囲が異なっており、（それに伴って）別の手法で同定・統合処理を行っているため 、CiNii Articlesの「参考文献」「被引用文献」の結果とも必ずしも一致していません。” (.txt char 3752)
- anchor cell draft: `G 参考文献／被引用文献 char 3646, char 3707, char 3752` (section heading `G 参考文献／被引用文献` at .txt char 3433; the three `char N` values are the located-quote offsets).

## Claim-support map (staged entry vs capture)

Rests on S087:
- Observation bullet 1, clause 1 (“参考文献 … are not necessarily the same as the paper's own references”): **supported** — `※CiNii Researchの「参考文献」は、実際の論文の参考文献と必ずしも一致していません。` (.txt char 3598).
- Clause 2 (“only those matched by 同定・統合処理 are shown”): **supported** — quote 1 (.txt char 3646).
- Clause 3 (“the reference count … is of the matched items, not the count printed in the paper”): **supported** — quote 2 (.txt char 3707).
- Clause 4 (“CiNii Research and CiNii Articles identify and merge differently, so the two services' lists need not match”): **supported** — quote 3 (.txt char 3752).
- Source line “section G 参考文献／被引用文献, the two 注意書き”: **supported** — heading at char 3433; the two ※ notes at chars 3598 and 3752.
- Inference bullet 1 (derived list, neither equal nor superset): **supported by premises** — quote 1 plus the 必ずしも一致していません clause.
- Inference bullet 2 (count is a matched-item count): **supported** — quote 2.
Nothing narrower or unsupported found for this row; no claim rests on S087 that the capture contradicts.

## Register row S082 re-check (chousa slice)

Register quote: `被引用文献（この論文を引用している文献）の一覧が表示されます。 随時増加していきます。`
- `.txt` count 0, `.raw` (UTF-8 HTML) count 0 — not verbatim in either form.
- Capture contains “参考文献（この論文が引用している文献）、被引用文献（この論文が引用されている文献）の一覧が表示されます。” (char 3448) and, separately, “随時増加していきます。” (char 3577).
- The register quote swaps the verb construction (を引用している vs が引用されている), drops the paired 参考文献 clause, and splices the independent “increases” sentence.

Verdict: **absent-as-written**. Source was fetched cleanly (reachable capture), so not `unverifiable`; the substance (cited-by list shown; grows over time) is genuinely on the page, so not fabricated — the quote is a rewritten splice. This matches round-48's recorded verdict (`round-48.md` Gate row S082: “capture contains a passive ‘cited by’ construction and a separate ‘increases’ phrase; register splices and reverses the relation”).

## Boundaries / hygiene

- Only write: this report. No production file, git index, jj state, fleet repo, sibling lane, or shokuknow artifact touched. No campaign tools run. No network. No tool installed (RULES.md read; no install expected).
- Scratch: none created; nothing to delete.

VERDICT: re-grounded staged row S087→lane S096 on capture 09fc63de41f293d43d631c46 (.txt form): three byte-exact single-occurrence quotes at chars 3646/3707/3752 draft the Gate block with anchor `G 参考文献／被引用文献 char 3646, char 3707, char 3752`; every S087-based entry claim is supported; register row S082 re-checked absent-as-written (round-48 verdict confirmed).
