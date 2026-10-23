# Draft — round-32 QUALITY addition for R1

Status: proposal only; append to `corpus/QUALITY.md` after criterion 32 (`corpus/QUALITY.md:242-248`), numbered 33. No lane production file was changed.

33. **A detector kill claim is receipt-backed.** Every lesson sentence saying a named detector “killed” or “caught” a named mutant cites the committed receipt(s) for that mutant and detector. For a count-based counter, each receipt used to support a kill must show `matched < total`; a nonzero `gate_rc` alone does not establish a kill, and a sentence grouping mutants maps each mutant to its own result. `matched == total` means the counter did not kill that mutant. — round-31 R1: `corpus/lessons/round-31.md:95-100`; `.ufo/waves/round-31/falsify/ReviewCorrD7D8.md:4`.

## R1 focused negative check

Run from the lane root. This focused regression checks the fail-open attribution from R1, not every possible Markdown kill claim:

`timeout 30 python3 -c 'import json,re,sys; from pathlib import Path; f=Path("corpus/lessons/round-31.md"); text=f.read_text(); items=[(text.count("\n",0,m.start())+1,m.group()) for m in re.finditer(r"(?ms)^- .*?(?=^- |\Z)",text)]; claims=[(n+body[:body.find("killed by the counter")].count("\n"),body) for n,body in items if "fail-open hashing (MutC2Hash)" in body and "killed by the counter" in body]; paths=sorted(Path(".ufo/waves/round-31/falsify/MutC2Hash").glob("failopen.mutated.*.receipt.json")); receipts=[json.loads(p.read_text()) for p in paths]; missing=bool(claims) and (not paths or any(p.name not in body for _,body in claims for p in paths)); over=bool(claims) and any(r["matched"]>=r["total"] for r in receipts); bad=missing or over; shown=", ".join(p.name+"="+str(r["matched"])+"/"+str(r["total"]) for p,r in zip(paths,receipts)); print(("FAIL" if bad else "PASS")+": "+("round-31.md:"+",".join(str(n) for n,_ in claims)+" calls fail-open counter-killed; "+("receipt citations missing; " if missing else "")+("all-match receipts: " if over else "")+shown if bad else "kill claims cite below-total receipts")); sys.exit(1 if bad else 0)'`

Observed on the uncorrected lesson and its receipts:

`FAIL: round-31.md:98 calls fail-open counter-killed; receipt citations missing; all-match receipts: failopen.mutated.3277349906142620654.receipt.json=120/120, failopen.mutated.9879869915017300514.receipt.json=120/120`

Exit code: 1. The committed-receipt check was `timeout 30 git rev-parse HEAD HEAD:.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.3277349906142620654.receipt.json HEAD:.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.9879869915017300514.receipt.json`; output was `4111607c857bc29ff31883bc095ae00afb527e50`, `0e9007688cddf2a190c63881cb890e2085f61650`, `af713f4b8f3d951f6e72591cd1ffcad5a708fb3c`. Both receipt JSONs at lines 9-14 show `gate_rc: 1`, `matched: 120`, `total: 120`, and `predicate_holds: true`.

## Proposed `## Mistakes` row

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| A detector-kill claim called fail-open hashing killed although both counter receipts are 120/120 (round 31 R1) | `corpus/lessons/round-31.md:97-98`; `.ufo/waves/round-31/falsify/MutC2Hash/failopen.mutated.3277349906142620654.receipt.json:11-14` and `failopen.mutated.9879869915017300514.receipt.json:11-14`; `.ufo/waves/round-31/falsify/MutC2Hash.md:5`; routed R1 at `corpus/lessons/round-31-verifier-spotcheck.md:203-208` | round-31 verifier spot-check, R1 | QUALITY 33; append a named correction that fail-open survived both detectors; retain span-before-stale as counter-killed/selftest-survived (110/120, `.ufo/waves/round-31/falsify/MutC2Hash.md:6`) and add the omitted whitespace-trim mutant as counter-killed/selftest-survived (118/120, `.ufo/waves/round-31/falsify/MutC2Parse.md:4`); cite the corresponding committed evidence. |

## Scope and limits

The one-line check is an R1-specific regression for a wrapped list item and its two fail-open receipts; it is not a general Markdown parser or an audit of every detector-kill claim. The separate evidence says fail-open survived the selftest (`.ufo/waves/round-31/falsify/MutSelftestNew31.md:17`, `.ufo/waves/round-31/falsify/MutC2Hash.md:5`), while the spot-check explicitly routes the incorrect attribution and the correction (`corpus/lessons/round-31-verifier-spotcheck.md:203-208`).