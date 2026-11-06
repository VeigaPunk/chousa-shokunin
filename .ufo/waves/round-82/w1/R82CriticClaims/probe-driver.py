#!/usr/bin/env python3
"""R82CriticClaims probe: K2/K3 generality tests against the landed gate and base gate.

Cases are authored by this seat (not in the frozen manifest). For each case the exact
frozen SKILL.md Run line text (base bytes) is executed in cwd=<tree> over the record.
"""
import os, re, shlex, subprocess, sys, textwrap

S = "/fast/scratch/hyaku/chousa-r82/R82CriticClaims"
LAND = os.path.join(S, "b4a41d251b488f06b4a6ab01a11bc12ce72edd20")
BASE = os.path.join(S, "5d792e1e953649e801d9bf1f64093b1f0d4dac8c")
WORK = os.path.join(S, "probe-records")
os.makedirs(WORK, exist_ok=True)

RUN2 = ('f=<r>; ! bash tools/research-gate.sh verify "$f" --root . | grep -q '
        "'^FINDING NEGATIVE_WITHOUT_SWEEP' && bash tools/research-gate.sh verify-sweeps \"$f\" --root .")
RUN4 = 'bash tools/research-gate.sh verify-sweeps <r> --root .'

ITEM4 = """# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | critic probe |

## Question

critic probe record

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | fleet-gate | corpus/fixtures/sweeps-r5.md | critic probe |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| N1 | negative | no pre-round knowledge entry file is named for the TARCiS statement | corpus/fixtures/sweeps-r5.md | observed-in-dump | W1 |

## {REJHEAD}

| id | ref | {REJHDR} |
|---|---|---|
| R1 | corpus/fixtures/sweeps-r5.md | {REASON} | {FLIP} |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | N1 | corpus/knowledge/*tarcis-r80*,corpus/knowledge/*tarcis-pre-r81* | zero matches |
"""

ITEM2 = """# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | critic probe |

## Question

critic probe record

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | fleet-gate | corpus/fixtures/sweeps-r5.md | critic probe |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| N1 | negative | no pre-round knowledge entry file is named for the TARCiS statement | corpus/fixtures/sweeps-r5.md | observed-in-dump | {SWEEP} |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | corpus/fixtures/sweeps-r5.md | a round-5 fixture is test data, not a source on citation searching | a fixture that quoted a citation-searching standard verbatim would flip this rejection |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | {CLAIMID} | {WHERE} | zero matches |
"""

REASON_OK = "a round-5 fixture is test data, not a source on citation searching"
FLIP_OK = ("a fixture that quoted a citation-searching standard verbatim would flip this rejection")
WHERE_OK = "corpus/knowledge/*tarcis-r80*,corpus/knowledge/*tarcis-pre-r81*"

def item4(reason=REASON_OK, flip=FLIP_OK, head="Rejections", hdr="reason | flip_condition"):
    return ITEM4.replace("{REJHEAD}", head).replace("{REJHDR}", hdr).replace("{REASON}", reason).replace("{FLIP}", flip)

def item2(sweep="W1", where=WHERE_OK, claimid="N1"):
    return ITEM2.replace("{SWEEP}", sweep).replace("{WHERE}", where).replace("{CLAIMID}", claimid)

def run(cmd, root):
    env = {k: v for k, v in os.environ.items() if not k.startswith("CHOUSA_")}
    p = subprocess.run(["bash", "-c", cmd], cwd=root, env=env, capture_output=True, text=True, timeout=300)
    findings = sorted(set(re.findall(r"^FINDING (\S+)", p.stdout + p.stderr, re.M)))
    return p.returncode, findings, p.stdout + p.stderr

CASES = []
def add(cid, family, item, text, expect, also_base=False):
    CASES.append(dict(id=cid, family=family, item=item, text=text, expect=expect, base=also_base))

VOCAB = ["", "-", "--", "---", "\u2014", "\u2013", "n/a", "na", "n.a", "none", "nil", "null",
         "tbd", "tba", "todo", "?", "??", "...", "\u2026", "x", "unknown", "not applicable",
         "same", "ditto", "see above", "idem",
         "`n/a`", "*tbd*", "_none_", '"nil"', "'null'", "N/A", "TBD.", "None", "TODO...", "  "]

# class generality: every declared value in each cell position
for v in VOCAB:
    tag = re.sub(r"[^A-Za-z0-9]+", "_", v) or "EMPTY"
    add(f"G4F-{tag}", "vocab-item4-flip", 4, item4(flip=v), "refuse")
    add(f"G4R-{tag}", "vocab-item4-reason", 4, item4(reason=v), "refuse")
    add(f"G2W-{tag}", "vocab-item2-where", 2, item2(where=v), "refuse")
    add(f"G2C-{tag}", "vocab-item2-sweep", 2, item2(sweep=v), "refuse")
    add(f"G2Cnc-{tag}", "vocab-item2-sweep-noclaimid", 2, item2(sweep=v, claimid=""), "refuse")

# K2(b): rejection kept under any heading containing "reject"
add("B-emptyflip", "k2b-reject-heading", 4, item4(head="Rejected sources", flip=""), "refuse")
add("B-placeholder-reason", "k2b-reject-heading", 4, item4(head="Rejected sources", reason="idem"), "refuse")
add("B-nested-heading", "k2b-reject-heading", 4, item4(head="Rejections considered", flip="n/a"), "refuse")

# K2(c): negative claim naming no declared sweep row
add("C-undeclared", "k2c-negative", 2, item2(sweep="SW9", claimid=""), "refuse")
add("C-undeclared-withsec", "k2c-negative", 2, item2(sweep="SW9"), "refuse")

# K2(a) strong: claim sweep cell is a declared placeholder but a Sweeps row names the claim
add("A-placeholder-cell-claimid", "k2a-claim-sweep", 2, item2(sweep="n/a"), "refuse", also_base=True)
add("A-placeholder-cell-x", "k2a-claim-sweep", 2, item2(sweep="x"), "refuse", also_base=True)
add("A-placeholder-cell-dashdash", "k2a-claim-sweep", 2, item2(sweep="--"), "refuse", also_base=True)

# K3 harm candidates: records the base gate passes and that carry no K2 form
add("H-rejectheading-why-col", "k3-harm", 4,
    item4(head="Rejected sources", hdr="why | flip"), "pass-at-base/refuse-at-landing", also_base=True)
add("H-rejectheading-why-flipcond", "k3-harm", 4,
    item4(head="Rejected sources", hdr="why | flip_condition"), "pass-at-base/refuse-at-landing", also_base=True)
add("H-prose-sweep-ref", "k3-harm", 2, item2(sweep="W1 (declared below)", claimid=""), "pass-at-base/refuse-at-landing", also_base=True)
add("H-criteria-section", "k3-harm", 4,
    """# research-record v1
<!-- chousa-record: v1 -->
## Meta
| key | value |
|---|---|
| window | loopback |
| fetch | none |
| note | critic probe |

## Question

critic probe record

## Sources

| id | tier | pointer | notes |
|---|---|---|---|
| S1 | fleet-gate | corpus/fixtures/sweeps-r5.md | critic probe |

## Claims

| id | kind | text | pointer | status | sweep |
|---|---|---|---|---|---|
| N1 | negative | no pre-round knowledge entry file is named for the TARCiS statement | corpus/fixtures/sweeps-r5.md | observed-in-dump | W1 |

## Rejection criteria

| criterion | state |
|---|---|
| a source is not used by a claim | rejected |

## Rejections

| id | ref | reason | flip_condition |
|---|---|---|---|
| R1 | corpus/fixtures/sweeps-r5.md | a round-5 fixture is test data, not a source on citation searching | a fixture that quoted a citation-searching standard verbatim would flip this rejection |

## Sweeps

| id | claim_id | where | observed |
|---|---|---|---|
| W1 | N1 | corpus/knowledge/*tarcis-r80*,corpus/knowledge/*tarcis-pre-r81* | zero matches |
""", "pass-at-base/refuse-at-landing", also_base=True)
# positive control for the new heading rule: complete rejection under a "reject" heading
add("P-rejectheading-complete", "positive", 4, item4(head="Rejected sources"), "pass-at-both", also_base=True)

def main():
    print(f"LAND={LAND}\nBASE={BASE}\nCASES={len(CASES)}")
    bad = 0
    for c in CASES:
        name = re.sub(r"[^A-Za-z0-9_.-]+", "_", c["id"]) + ".md"
        rp = os.path.join(WORK, name)
        open(rp, "w").write(c["text"])
        cmd = (RUN2 if c["item"] == 2 else RUN4).replace("<r>", shlex.quote(rp)).replace("<record.md>", shlex.quote(rp))
        rc, finds, out = run(cmd, LAND)
        refused = rc == 1
        fam = c["family"]
        if fam.startswith("vocab") or fam.startswith("k2"):
            good = refused
        else:  # k3-harm / positive
            good = None
        line = f"CASE id={c['id']} family={fam} item={c['item']} rc={rc} findings={','.join(finds) or '-'} refused={'yes' if refused else 'no'}"
        if c["base"]:
            brc, bfinds, _ = run(cmd, BASE)
            line += f" base_rc={brc} base_findings={','.join(bfinds) or '-'}"
        if good is not None:
            line += f" verdict={'ok' if good else 'VIOLATION'}"
            bad += 0 if good else 1
        print(line)
    print(f"VIOLATIONS={bad}")

if __name__ == "__main__":
    main()
