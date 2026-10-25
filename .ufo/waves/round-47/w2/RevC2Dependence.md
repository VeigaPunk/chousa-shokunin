ATTACKS: C2 dependence leg — BARE bare-name resolution (round47/c2-count.py:92-94,180-187): soundness, pulled-path enumeration/classification, missed `$VAR/` / `os.path.join` calls
VERDICT: holds

Scope: lane tip 1fc5ed193ad48a482402c862f4e4cc47e46d5b2d extracted verbatim to /tmp/chousa-r47w2-RevC2Dependence/tree (git archive). No production file touched. Scratch copied to /tmp/chousa-r47w2-RevC2Dependence/ (will be removed before finishing).

1. What the BARE rule is (c2-count.py:92-94)
   BARE = `(?<![\w.-])[A-Za-z0-9_][A-Za-z0-9_.-]*\.(?:py|sh)\b`; at :180-187 every bare token in an entry-point source is resolved against `f.parent` (the source file's own directory) and added when the target exists and differs from the source.

2. Diff with vs without BARE on the /tmp tree (verbatim)
   WITH_BARE 94 WITHOUT_BARE 93
   BARE_ONLY: ['corpus/evidence/round26-registry-oracle.py']
   So BARE adds exactly one path. The two dependence-leg additions printed by the counter are:
   - corpus/evidence/round25-meta-oracle.py — already found by the round-46 NAMED regex (literal full path in round25-meta-differential.sh:40), not BARE-only;
   - corpus/evidence/round26-registry-oracle.py — the BARE-only addition.
   (Freeze-time counter on same tree, for reference: ENTRY_POINTS=93 abc=85 dependence=+1 check_named=+7 GATES_ROWS=46 C2=PASS; final: 94/85/+2/+7/51 P2=PASS. `MISMATCHES=0` and `ENTRY_POINTS≥FLOOR(92)` hold under both; the 93-vs-94 delta is the disclosed sum of freeze→final counter repairs, lesson round-47 mistake 3.)

3. Is the BARE-only path a real dependency? Yes — executed.
   round26-registry-differential.sh:9 `ORACLE=$SCRIPT_DIR/round26-registry-oracle.py` (sha256 852a7648...), executed at :74 `if python3 "$ORACLE" "$dir" --root "$root" --registry "$registry" >...`. NAMED cannot capture it: it matches `SCRIPT_DIR/round26-registry-oracle.py`, whose file check fails; BARE strips the `$SCRIPT_DIR/` prefix and resolves the basename against the script's directory — exactly the docstring example (:93). Correct behavior.

4. Classification of all 45 BARE matches (target exists, already in eps via legs A/B/C/E):
   Real call: round25-meta-oracle.py (round25-meta-differential.sh:40 `run(["python3","corpus/evidence/round25-meta-oracle.py",p],strict)`), round26-registry-oracle.py (:9/:74), research-gate.sh (tools/argv-witness.py:33 usage and :293 `--gate` default; tools/mechanism-witness.py:34, :229), quarantine-check.py (tools/absent-split.py:46 `GATE = LANE / "tools" / "quarantine-check.py"`).
   Real read/load: qr_harness.py (round30/c1-count.py:340 and c2-count.py:220 `sha256(os.path.join(HERE,"qr_harness.py"))`), verify-receipts.py (round38/c2-count.py:50, round39/c1-count.py:51, round39/c2-count.py:46, :381), c1-count.py (round38/c2-count.py:283 and round39/c2-count.py:370 `--counter` defaults; round42/43 quarantine-check reads are covered by leg A).
   Mere mention (comment/docstring/dict-key/usage line): round25-ledger-recount.py (round25-measure.sh:75 registry-coverage string check), round27-regressions.py (round27-falsify-controls.py:9 docstring), qr_harness.py (round30 c1/c2:12 docstrings), c1-count.py/c2-count.py (round30/qr_harness.py:2 docstring), c1-count.py/c2-count.py/c1-count-v2.py (round32/33/34 v2/v3 docstrings), verify-receipts.py (round38/c2:22, round39/c1:33, round39/c2:13,:23; round38/39 verify-receipts.py dict keys :61/:62, :53/:55), round37/c1-count.py comment example (round38/c2-count.py:30), mechanism-witness.py (tools/argv-witness.py:4 docstring).
   None of the mention-only hits changes the set: every one of those files is already registered by legs A (tools/), B (`c\d+-count[\w.-]*\.py` under corpus/evidence/round*/) or C/E. Net effect of BARE on this tree = one genuine execution.

5. Over-approximation risk (latent, not observed):
   BARE does not know comments/docstrings from code. On a tree where a docstring-only bare mention names an existing adjacent script that is NOT otherwise registered, it would add a non-gate to ENTRY_POINTS (registry inflation). Also, `os.path.join(HERE,"..","round37","c1-count.py")` (round38/c2-count.py:51; round39/c2-count.py:49 analog) resolves the bare `c1-count.py` to the WRONG local sibling (round38/c1-count.py, round39/c1-count.py). Both wrong-sibling and true-target files exist and are registered (leg B), so nothing is lost today; the mis-resolution is latent. `.pyc` cannot match (`\b` after `py` fails before `c`); generated fixtures under `$WORK`/`$TMP`/`$tmp`/`root`/`work` are outside the repo and are skipped by the `relative_to`/`is_file` guards.

6. Missed real calls — scan results: no gaps found.
   - No literal `../`-relative repo-file refs anywhere in eps sources (scan: zero hits aside from c2-count.py's own comment).
   - All `$VAR/`-composed paths in eps sources target: research-gate.sh (round24/25/26-measure.sh, round26-date-differential.sh, round26-registry-differential.sh:16, controls) — registered by leg A; ORACLE — covered by BARE (above). No other.
   - All `os.path.join(LANE/HERE, ...)` repo-script compositions target tools/quote-reopen.py (round30 c1/c2 :277 default; leg A), tools/quarantine-check.py (leg A), roundNN/cN-count.py siblings (leg B; BARE's wrong-sibling resolution is masked because both siblings exist), verify-receipts.py same-dir (NAMED + BARE).
   - subprocess/Popen/run( targets: only `["bash", gate, ...]` where gate defaults to `tools/research-gate.sh` (argv-witness.py:328, mechanism-witness.py:262) — leg A; `[sys.executable, str(TOOL), ...]` with TOOL=LANE/"tools"/"quarantine-check.py" (round42/c1-count.py:31,76; round43/c2-count.py:38) — leg A.
   - tools/research-gate.sh itself invokes only `python3 -c` (inline JSON validation, lines 5550-5554, 6691-6695, 7890-7894, 7921-7925); no repo-script invocation to miss.
   - No `source`/`.` invocations with composed paths in any eps source.

7. Bottom line: BARE is sound in effect on the frozen tree — its sole unique addition is a real executed dependency, and no real executed/read path is missed. The counter's dependence leg holds. Risk notes (latent only): comment/docstring mentions are matched by BARE and could inflate ENTRY_POINTS if unregistered; sibling mis-resolution for `os.path.join(HERE,"..",...)` is masked by leg B today.
