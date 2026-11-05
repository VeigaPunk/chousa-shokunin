# R79CriticA — round-79 W1 critic: falsify the claim text, not the instruments

Lane `chousa-shokunin`; base `ee70e6df19fe43b1b384166cf5d360c3b99dafe2`; controls commit
`e2bf2bbb5ca66f06b6571cbcaa15554d1a74a67c`; frozen claims at `b58a02db` (`corpus/evidence/round79/claims.md`).
Leaf seat: read-only on the lane, every mutation inside one `git clone --shared` under
`$HYAKU_SCRATCH/chousa-r79/R79CriticA/`. No production edit, no commit, no network.

## Axes

1. **Claim-text fidelity** — does the frozen sentence name the event the kill rule names?
2. **Kill-rule reach** — does the predicate's enumeration cover every universal clause?
3. **Provenance** — is each quoted receipt re-derivable, at a pinned revision, from committed bytes?
4. **Separability** — does each claim verify without the other's bytes?

All four instruments and their nine digests match the frozen table exactly
(`sha256sum` over `git show e2bf2bbb:<path>`; the table in `claims.md:8-21` is reproduced
byte-for-byte). Provenance of the *instruments* is sound. The findings below are about the
*claims*.

## Reproductions (every value below was re-derived in scratch, not read from the receipt)

| command | receipt | observed |
|---|---|---|
| `forge-battery.py --battery round79/matrix-battery-v6.py --work DIR` | `R79CriticA/forge-battery-after-v6.txt` | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`, exit 0 — **matches** `claims.md:60` |
| `forge-battery.py --battery round78/matrix-battery-v5.py --work DIR` | `R79CriticA/forge-battery-before-v5.txt` | `FORGE_BATTERY=FAIL forgers_handled=5/6 positive=1/1`, exit 1; line 9 `FORGER a8-v5-salt-normalizer … verdict=FORGED` — **matches** `claims.md:55-56` |
| `derivative-check.py --battery …v6.py` | `R79CriticA/derivative-after-v6.txt` | `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23`, exit 0 — **matches** `claims.md:61` |
| `derivative-check.py --battery …v5.py` | `R79CriticA/derivative-before-v5.txt` | `DERIVATIVE_COPIES=13/13 MAX_WINDOW=4096`, exit 1 — **matches** `claims.md:57` |
| `selfcheck-v2.py --lane . --rev ee70e6df…` | `R79CriticA/selfcheck2-before.txt` | `SELFCHECK2=FAIL unresolved=3/3`, exit 1; `missing=[116]` |
| `selfcheck-v2.py --lane .` (HEAD `b58a02db`) | `R79CriticA/selfcheck2-after.txt` | `SELFCHECK2=PASS unresolved=0/3`, exit 0 — **matches** `claims.md:106` |
| `round78/selfcheck.py --lane . --rev ee70e6df…` | `R79CriticA/selfcheck-v1-before.txt` | `SELFCHECK=PASS unresolved=0/3`, exit 0 — **matches** `claims.md:97` |
| `selfcheck-control.py --lane . --work DIR --base ee70e6df…` | `R79CriticA/selfcheck-control-repro.txt` | `CONTROL=PASS cases=4 v1_false_greens=2/2 v2_refusals=2/2`, exit 0 — **matches** `claims.md:101` |

Separability, both directions:

| probe | receipt | observed |
|---|---|---|
| every C1 file deleted and staged, C2 measured | `R79CriticA/selfcheck2-without-c1-files.txt` | `SELFCHECK2=PASS unresolved=0/3`, exit 0 — C2 verifies without C1 |
| `SKILL.md`, `corpus/QUALITY.md`, `corpus/lessons/round-77.md` at base, C1 measured | `R79CriticA/forge-battery-v6-without-c2-repairs.txt` | `FORGE_BATTERY=PASS forgers_handled=6/6 positive=1/1`, exit 0 — C1 verifies without C2 |

**Answer to Q6: yes, in both directions.** Neither claim's predicate reads the other's bytes.

## The six questions

### C1 — operability (`claims.md:23-72`)

**(1) Same event?** Partly. The sentence (`claims.md:29-33`) names four events: (i) v5's copy is
recovered byte-for-byte by one normalizer, (ii) no 40-byte window of a v6 copy occurs in its
committed source, (iii) the positive matrix is accepted, (iv) one text-level normalizer per salt
family is refused. The kill rule (`claims.md:63-68`) names (ii) as clause 4, (iii) as clause 2,
(iv) as clause 3 ("if any forger is FORGED") — and never names (i). A claim half with no kill
clause is the round-78 routed-defect-1 shape (`corpus/lessons/round-78-verifier-spotcheck.md:186-188`)
surviving on the *before* half. It happens to be true (`v5-byte-exact-recovery.txt`,
`EXACT_RECOVERY=13/13`), but nothing in the kill rule could have falsified it.

**(2) Genuine do-nothing control?** Yes. At base the only battery on disk is v5; I re-ran it and
got `handled=5/6` at exit 1 with `a8 … verdict=FORGED` (`forge-battery-before-v5.txt`). A round
that does nothing cannot reach the target.

**(3) After-state, one command, committed bytes?** The *predicate* is one command and one value,
re-derived at `b58a02db` (exit 0). The *kill rule* is not: clause 4 needs
`derivative-check.py`, a second command (`claims.md:48-52` names it, so this is a reading cost,
not a contradiction).

**(4) Universal clause not enumerated?** **Yes, and it fires.** "if any forger is FORGED"
(`claims.md:64`) is universal; `forgers_handled=6/6` enumerates six. A seventh forger is FORGED
on these bytes (finding **F4**).

**(5) Axis by surface, not number?** Yes — `claims.md:25-27` names the copy mechanism
("The round changes the *outer battery's copy mechanism*, not the number the lane reports").

**(6) Separable?** Yes, measured above.

### C2 — calibration (`claims.md:74-116`)

**(1) Same event?** On paper yes: the sentence's "audits every block, so neither false-green
survives" (`claims.md:81-82`) is the kill rule's clause 3 ("a newer `## Round-<n> addition` block
hides an earlier criterion from the audit", `claims.md:111-112`). The instrument does not deliver
clause 3 (finding **F1**), and the sentence's "validates every repair line" is broader than the
instrument (finding **F3**).

**(2) Genuine do-nothing control?** Yes. `selfcheck-v2.py --lane . --rev ee70e6df…` prints
`SELFCHECK2=FAIL unresolved=3/3` exit 1 on the base bytes (`selfcheck2-before.txt`), and the
predecessor prints PASS on the same bytes (`selfcheck-v1-before.txt`). A do-nothing round cannot
reach the target.

**(3) After-state, one command, committed bytes?** Yes for the value; no for the pin. The after
receipt prints `REV=worktree`, not a revision (`controls/selfcheck2-after.txt:1`), so the value is
not re-derivable from a *pinned* revision — round-78 routed defect 9's class
(`round-78-verifier-spotcheck.md:216-219`). My worktree re-run at `b58a02db` matches, so the value
is right and only the label is wrong (finding **F8**).

**(4) Universal clause not enumerated?** Two. "validates every repair line against the bytes it
names" — `check_skill` validates a `correction:` line only when its named line is *currently
malformed* (`selfcheck-v2.py:172`); a repair line naming a non-defective row is never validated.
"audits every block" — `criteria()` scans every block, but a duplicate criterion number overwrites
the earlier occurrence (`selfcheck-v2.py:146`), so "every block" is true and "every criterion" is
false.

**(5) Axis by surface, not number?** Yes — `claims.md:76-77` names the surface ("the lane's
self-assessment read against observed repo state … it is not an assertion").

**(6) Separable?** Yes, measured above.

## Findings

### F1 — C2 kill rule fires: a newer block still hides an earlier criterion (HIGH)

`criteria()` keys criteria by number in a dict; `out[current] = [line]` (`selfcheck-v2.py:146`)
overwrites an earlier criterion that carries the same number. A newer `## Round-<n> addition`
block that re-uses a number therefore deletes the earlier criterion from the audit — the exact
event `claims.md:111-112` names.

Input: HEAD `b58a02db`, remove ` supersedes: 116 digest=ae134338138ad3e0` from criterion 149, append

```
## Round-999 addition

116. **A duplicate criterion number whose pointers resolve.** corpus/QUALITY.md
```

Observed (`selfcheck2-duplicate116-head.txt`):

```
CHECK S2-quality-pointers ok criteria=50 missing=[] superseders={} unresolved=[]
SELFCHECK2=PASS unresolved=0/3
# exit: 0
```

while criterion 116's pointer is still live (`quality-gapdump-base.txt`: `116: gaps=['corpus/evidence/round59/claims.md']`;
the file is absent at both revisions). The same block on the *unrepaired* base tree hides the
defect from the audit too (`selfcheck2-duplicate116-base.txt`: `missing=[]`, `criteria=49` — the
count does not even move). **Kill rule clause 3 fires: the successor prints PASS with the defect
present.**

Smallest safe correction: `criteria()` must not collapse duplicates — return the duplicate ids and
add them to `unresolved` (one clause in `check_quality`), and add this input as a third control
case beside `hollow` and `window`.

### F2 — C2's class provenance is false: routed defect 3 is not audited, and 102/103 are not defects (HIGH)

`claims.md:89-93` says the three classes are the round-77 spot-check's routed defects 1, 3 and 4,
and that the QUALITY class is "116, plus 102 and 103 which the wider audit also resolves".

- Routed defect 3 is **criterion 142**, not 116 (`corpus/lessons/round-77-verifier-spotcheck.md:169-173`).
  Its pointer `receipts/02c-work-unwritable.*` still resolves to nothing
  (`git ls-files | grep -c 02c-work-unwritable` → `0`; all three `receipts/02c-*` / `02b-*` paths
  `MISSING`). The counter cannot see it: `pathlike()` rejects any token containing `*`
  (`selfcheck-v2.py:107-112`), so 142 prints `gaps=[]`. The class the claim says it carries is
  never audited.
- 102 and 103 have no gaps at all (`quality-gapdump-head.txt`: `102 … gaps=[]`, `103 … gaps=[]`),
  and the frozen receipt prints `missing=[116]` (`selfcheck2-before.txt:3`). The parenthetical
  contradicts the receipt it cites. The lane's own lesson records the provenance of the
  confusion: the first all-block sweep reported 18 unresolved, 17 false, then "re-measured
  `missing=[116]` (one true defect)" (`corpus/lessons/round-79.md:50`).

Smallest safe correction: `claims.md:91-92` becomes "the `QUALITY.md` criterion whose backticked
pointer resolves to no committed path (criterion 116)"; routed defect 3 moves to the recorded
limits as "not audited — `pathlike()` excludes glob tokens".

### F3 — C2 sentence overstates the repair-line validation (MEDIUM)

`claims.md:81-82`: "the successor validates every repair line against the bytes it names (digest)".
`check_skill` iterates `for n, line in malformed` (`selfcheck-v2.py:172`) and validates a repair
only for a line that is defective *now*; a `correction:`/`erratum:` line naming a clean line is
never checked against anything. The universal is enumerated over currently-defective targets only.
No false green follows from this alone (an unvalidated line resolves nothing), but the sentence is
not what the instrument does.

Smallest safe correction: "validates every repair line whose target is currently defective against
the bytes it names".

### F4 — C1's sentence is falsified: a two-step text decode recovers subject identity, and the predicate still passes (HIGH)

The v6 copy is `WRAPPER.format(payload=base85(marshal(code)))` (`matrix-battery-v6.py:277-281`).
The payload is *text*; decoding it is a text operation. `_rename` renames bound identifiers only,
so every string constant survives re-emission.

Probe `a10-payload-decode.py` (copied to `R79CriticA/a10-payload-decode.py`): regex the
`b85decode('…')` literal → `base64.b85decode` → `marshal.loads` → walk `co_consts` → identify by the
surviving string constants against a table built statically from the committed sources with
`ast.parse`. No identifier canonicalisation, no subject execution, no scoring.

- Identification: **13/13 correct** on fresh copies of all thirteen subjects, Jaccard 0.50–0.93
  (`a10-identification.txt`).
- Verdict against the committed battery: `BATTERY=PASS forgers_rejected=11/11 positive=2/2
  oracle=REJECTED`, exit 0 (`a10-receipt.txt`) — the battery's own exact target line, reached
  without reading a single subject's behaviour.

So the claim's words "the round-79 battery's copy is not [a textual derivative of a committed
file]" (`claims.md:31-32`) are false: a committed source's compiled form is recovered from the
copy's text with two library calls, and its identity is recovered from the constants that survive
renaming. The carve-out (`claims.md:65-68`) names "unmarshal the payload **and canonicalise the
fresh identifier table**"; `a10` unmarshals and never canonicalises, because it does not need to.
The carve-out's named event is narrower than the attack, so it does not cover this input.

**Is it a claim failure or a recorded limit?** Both readings are live, and that is the defect:
- the kill rule's clause 3 is universal — "if **any** forger is FORGED" (`claims.md:64`) — while the
  predicate enumerates six (`forgers_handled=6/6`). Under the rule's literal words, `a10` is
  FORGED and **C1 fails**;
- under the instrument's six-forger scope, `a10` is a recorded limit — but one the carve-out
  mis-describes, and one the claim says is "measured by the wave" (`claims.md:67`) when no
  committed forger or receipt measured it at the freeze: the three extra files in
  `corpus/evidence/round79/forgers/` are `forge-order-matrix*.py`, call-count *matrix* probes that
  never read a copy. `a10-receipt.txt` is the first measurement of the channel, supplied here.

Smallest safe correction: `claims.md:64` reads "if any of the six enumerated forgers is FORGED",
and the carve-out's event becomes "payload decoding (b85decode + marshal of the wrapper literal),
which recovers subject identity from the surviving string constants without canonicalisation".

### F5 — the `a9` half of "one normalizer per salt family" is tautological (MEDIUM)

`a9` deletes the wrapper's three fixed lines and hashes the remainder. On every v6 copy the
remainder is the empty string: `copy_lines=3 a9_kept_lines=0 digest=e3b0c44298fc` for all thirteen
subjects (`a9-empty-normalisation.txt`; `e3b0c442…` is `sha256("")`). Its refusal is therefore a
property of the wrapper having three lines, not a measurement of the textual channel — it is
symmetric with `a8` in form and empty in content. `claims.md:33,43-44` is true but carries no
information beyond "the copy is a wrapper", which is exactly what F4 then defeats.

Smallest safe correction: state the `a9` channel as "a text normalizer that does not decode the
payload sees no text" and pair it with the decoding probe, which is the discriminating one.

### F6 — C1's before half has no kill clause (MEDIUM)

`claims.md:29-31` asserts the v5 copy is recovered byte-for-byte by one normalizer. It is true
(`v5-byte-exact-recovery.txt`: `EXACT_RECOVERY=13/13`, including the two public positive digests
`9334721a…` and `909987ce…` that `a8` matches), but the kill rule (`claims.md:63-65`) names no
before-state event. Covered only indirectly by "any copy shares a 40-byte window", which fires on
v5 at `MAX_WINDOW=4096`. Round-78 routed defect 1 asked that the target sentence and the kill rule
name the same event; the before half still does not.

Smallest safe correction: add "if the v5 receipt is not `handled=5/6` exit 1 with `a8` FORGED, or
if a v5 copy is not recovered byte-for-byte by the salt-family normalizer".

### F7 — derivative-check measures worktree bytes, the claim says "committed source" (LOW)

`claims.md:32` says "no 40-byte window of a copy occurs in **its committed source**";
`derivative-check.py:94` reads `source.read_bytes()` from the path handed in, i.e. the worktree, not
`git show <rev>:<path>`. On a clean tree the bytes are identical (verified: all nine instrument
digests match `e2bf2bbb`), but a dirty tree silently changes the referent of the claim's own noun.

Smallest safe correction: read the source through `git show <rev>:<path>` and print the revision.

### F8 — the C2 after receipt is unpinned (LOW)

`controls/selfcheck2-after.txt:1` prints `REV=worktree`. The value is correct (I re-derived it at
`b58a02db`), but a closure cannot re-derive it from a named revision. Round-78 routed defect 9 is
the same class. The claim's other after receipt (`forge-battery-after-v6.txt`) does print
`BATTERY_SHA256` and `CC`, so the pair is inconsistent.

Smallest safe correction: re-measure with `--rev b58a02db…` (or the landing revision) so the line
reads a revision.

## Strongest sentence, and its verdict

**C2** — "the successor validates every repair line against the bytes it names (digest) and audits
every block, so neither false-green survives" (`claims.md:81-82`). Input: a newer block that reuses
a criterion number. The earlier criterion disappears from the audit, the counter prints
`SELFCHECK2=PASS unresolved=0/3` exit 0, and the defect it names is still present. **Claim failure:
kill rule clause 3 fires** (`claims.md:111-112`). This is the stronger of the two, because it needs
no new instrument — only a text append.

**C1** — "the round-79 battery's copy is not [a textual derivative]" (`claims.md:31-32`). Input: any
v6 copy, decoded with `b85decode` + `marshal.loads`. Identity is recovered 13/13 and the battery's
exact target line is reached at exit 0 while `DERIVATIVE_COPIES=0/13 MAX_WINDOW=23` holds.
**Recorded limit under the six-forger scope; claim failure under the kill rule's literal "any
forger"** — the ambiguity is the defect.

## QUALITY criteria the claims are read against

- **143** (`corpus/QUALITY.md:1046`) — "no invertible answer key, no strippable subject identity and
  no receipt a child can append to; its predicate is bound to the exit code". The v6 wrapper *is* an
  invertible encoding of the code object (F4); the round closed the strippable-salt and append
  channels, not the invertible-payload one.
- **145** (`:1052`) — the exit-code-plus-trailer binding. Holds: `RECEIPT_LINES=113` and the
  predicate line reproduce; `a5d` is DETECTED.
- **146** (`:1054`) — "validates each resolution line against the bytes it claims to repair, and its
  audit window covers every block rather than the newest". The digest binding holds for the
  currently-defective target; the audit window is block-wide but not criterion-wide (F1), and the
  class list is not the audited set (F2).
- **147** (`:1056`) — "a subject-identity salt is defeated by any normalizer that knows its marker
  family, so the closure is a per-channel measurement and not a property of the salt". v6 replaced
  the salt with a payload; the marker family is now the three-line wrapper, and the normalizer that
  knows it is `a10` (F4). 147's own lesson applies unchanged to v6.
- **148** (`:1058`) — missing tool maps to exit 2. Not exercised by either predicate; unchanged.
- **149** (`:1062`) — the superseder rule. `supersedes: 116 digest=ae134338138ad3e0` matches
  `sha256(body(crit[116]))[:16]` and 149's own pointers all resolve (`quality-gapdump-head.txt`),
  so the repair is genuinely digest-bound. The rule is sound; the *audit* around it is not (F1).
- **Round-78 routed defect 1** (`round-78-verifier-spotcheck.md:186-188`) — "C1's claim text and its
  kill rule contradict each other … round 79 must restate the claim so the target sentence and the
  kill rule name the same event". C1's *after* half now names the same operational event (40-byte
  window); its *before* half does not (F6), and the universal "any forger" is still unenumerated
  (F4). Partially closed.

## Scratch and tooling

Scratch: `/fast/scratch/hyaku/chousa-r79/R79CriticA/` (`HYAKU_SCRATCH` unset, default
`/fast/scratch/hyaku`), one `git clone --shared`, deleted before yield. No tool installed or
upgraded: every command used the host `python3` standard library and `git`; no pacman, no `uv`, no
network. No file written outside the wave output folder and that scratch dir.
