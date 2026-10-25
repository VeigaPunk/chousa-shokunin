#!/usr/bin/env python3
"""make-w3-spec.py — build the round-44 wave-3 spec from a fixed item table.

Contract: reads the godspeed directive bytes verbatim, writes one wave spec
JSON with pairwise-distinct item texts. No network. Exit 0 on write, 2 on
usage. The spec is validated afterwards by ufo-swarm-wave.mjs; this script
does not validate.
"""
from __future__ import annotations

import json
import pathlib
import sys

DIRECTIVE = pathlib.Path("/home/vgpnk/.agents/skills/godspeed/directive.md")
OUT = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/w3-spec.json"
)

LANE = "/home/vgpnk/Projects/shokunin/chousa-shokunin"
WAVE = "/home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-44/w3"

CONTEXT = f"""# Goal
chousa lane, round 44, wave 3 — falsify what wave 2 and the freeze commit landed.
Lane repo: {LANE}. Frozen claims: {LANE}/corpus/evidence/round44/claims.md.
Do not retune a predicate, a counter, a quote or a target: the claims were frozen
before any seat scored and a rule changed after a seat scored is not the claim's rule.
Wave 1's 64 seats died at spawn on a usage error and wave 2's parent receipt was
truncated when the orchestrator process died. Those 64 wave-1 names stay dead and
are not replaced. This wave does not replace them either.

# Seat contract
- You are a leaf. Do not spawn, dispatch, or start background work.
- Write ONLY your report at the absolute path named in your item, under {WAVE}/.
- Every `Report:` trailer path is relative to {LANE} — write it at {LANE}/<that path>.
- Never modify lane production files, the lane git index, jj state, the fleet repo,
  a sibling repo, or /home/vgpnk/Projects/shokuknow.
- NO network. NO fetch. NO curl. NO wget. NO urlopen. L0 `8d77e6c1` is still open,
  so no new external fetch is permitted this round.
- Tooling: you may install a tool that helps, after reading
  /home/vgpnk/.omp/agent/RULES.md for the official-source/channel policy, the host
  update-safety gate and the installation-record requirement. Pacman is PAUSED
  host-wide: do not run pacman -S, -Sy, -Syu, -U, -R, or downgrade, and do not
  restart a host service. Install via uv tool / npx / an official binary in
  ~/.local/bin, or file an L0 question instead.
- Never pass or hardcode a model. The planner seat is the L1; you are a leaf.
- Scratch files go under /tmp only. Never write a scratch file into the lane tree.
- Quote command output. An unrun check has not passed. Stop after the report.
"""

ITEMS: list[tuple[str, str, str]] = [
    # ---------------- attack seats ----------------
    (
        "W3RevReceipt",
        "reviewer",
        "Attack C1's receipt integrity. Run "
        f"python3 {LANE}/corpus/evidence/round44/c1-count.py and paste stdout and the exit code. "
        f"Then read {LANE}/corpus/evidence/round44/parent-lifetime.receipt and quote its "
        "'start parent_pid=' line and its 'end parent_pid=' line, and count the "
        "'spawn name=' lines and the 'reap name=' lines. State whether the two parent pids "
        "are the same number and whether the two counts are equal.",
    ),
    (
        "W3RevDisp",
        "reviewer",
        "Attack C2's no-blind-sweep promise. Independently re-verify 10 rows of "
        f"{LANE}/corpus/evidence/round44/disposition.tsv: for each of the first 10 rows, "
        "recompute the sha256 of the file at the recorded path, check the basename stem "
        "appears inside that file, and check a round token (40 or 41) appears in it. "
        "Paste a table of 10 rows: path, computed sha256, recorded sha256, stem present, "
        "round token present. Name every mismatch.",
    ),
    (
        "W3RevS079",
        "reviewer",
        "Attack C3's row normalization. Read the S079 row of "
        f"{LANE}/corpus/SOURCES.md. Count the number of columns it splits into on '|' and "
        "say whether any cell contains a literal or escaped pipe. Then confirm that "
        f"{LANE}/corpus/knowledge/citation-version-binding-r36.md cites 'source: S079' and "
        "does not cite 'source: S081'. Quote the citation line.",
    ),
    (
        "W3RevLesson",
        "reviewer",
        "Attack the assimilation Gate contract. Read "
        f"{LANE}/corpus/lessons/round-44.md and quote its '## Gate' block's admit entries "
        "and reject entries. State whether the block records at least one admit and at "
        "least one reject, and whether each reject carries a reason and a flip condition. "
        "Paste the four lines you quote.",
    ),
    (
        "W3CritForge",
        "critic",
        "Attack C1's cheapest full-marks gate. Read "
        f"{LANE}/corpus/evidence/round44/c1-count.py and the 'Cheapest full-marks gate' "
        "paragraph of "
        f"{LANE}/corpus/evidence/round44/claims.md. Then BUILD the forgery in /tmp only "
        "(never inside the lane tree): a receipt whose start and end parent_pid are the "
        "same number, whose child pids are all invented but positive, and whose 64 names "
        "are copied from "
        f"{LANE}/corpus/evidence/round44/seat-names.txt. Run the counter against that "
        "forgery with --receipt and paste stdout and the exit code. State plainly what "
        "the counter proves and what it does not prove.",
    ),
    (
        "W3CritBlind",
        "critic",
        "Attack C2's kill rule. On copies under /tmp only, run two mutations of "
        f"{LANE}/corpus/evidence/round44/disposition.tsv: (a) delete the reason text of one "
        "reverified-commit row and keep the rest, (b) mark one of the three modified-path "
        f"rows as reverified-commit. Run python3 {LANE}/corpus/evidence/round44/c2-count.py "
        "--table against each copy and paste both stdouts and both exit codes. Say whether "
        "the counter catches each mutation.",
    ),
    (
        "W3CritFresh",
        "critic",
        "Attack the freshness self-grade from the opposite direction of the wave-2 seat. "
        "List every axis-move this round could have claimed and show which ones are NOT "
        "available without a live re-check after "
        "2026-10-24T21:36:37-03:00. Then state the exact sentence the round-44 SCORECARD "
        "freshness cell must contain. Do not edit SCORECARD.md. Also quote the round-43 "
        f"route 2 sentence from {LANE}/corpus/lessons/round-43-verifier-spotcheck.md.",
    ),
    (
        "W3CritScope",
        "critic",
        "Attack write scope and adjacency. Run "
        f"git -C {LANE} status --porcelain and list every path, stating for each whether it "
        "is inside the lane tree or outside it. Then confirm that nothing under "
        "/home/vgpnk/Projects/shokuknow was modified by this round: list the mtime of "
        "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache and of the "
        "merge/chousa package files you read. Paste both.",
    ),
    (
        "W3MutC1",
        "mutation-tester",
        "Mutate C1. On copies under /tmp only, take "
        f"{LANE}/corpus/evidence/round44/parent-lifetime.receipt and (a) set one "
        "'child_pid=' to 0, (b) change the 'end parent_pid=' value to a different number "
        "than the 'start parent_pid=' value. Run "
        f"python3 {LANE}/corpus/evidence/round44/c1-count.py --receipt against each copy "
        "and paste both stdouts and both exit codes.",
    ),
    (
        "W3MutC2",
        "mutation-tester",
        "Mutate C2. On copies under /tmp only, take "
        f"{LANE}/corpus/evidence/round44/disposition.tsv and (a) change one "
        "reverified-commit row's sha256 to a wrong value, (b) delete one row entirely. Run "
        f"python3 {LANE}/corpus/evidence/round44/c2-count.py --table against each copy and "
        "paste both stdouts and both exit codes.",
    ),
    (
        "W3RevRouted",
        "revenger",
        "Attack the r43 closure routes. Read the '## Routed defects' section of "
        f"{LANE}/corpus/lessons/round-43-verifier-spotcheck.md. For each of its three "
        "items, state whether this round's bytes answer it and quote the answering file and "
        "line. Then name the routed item that is still open and why. Also state which of "
        "the three items this round did not touch.",
    ),
    (
        "W3SentNet",
        "sentinel",
        "Attack the fetch-scope guard. Search every file this round added under "
        f"{LANE}/corpus/evidence/round44/, {LANE}/corpus/knowledge/, {LANE}/tools/ and "
        f"{LANE}/.ufo/waves/round-44/ for a network call: grep -nE 'urlopen|urllib|requests\\.|curl |wget |socket\\.' "
        "over the .py and .sh files. Report every hit with its file and line, and say for "
        "each whether it is a live call or only a citation string or a comment. Do not "
        "fetch anything.",
    ),
    # ---------------- build seats ----------------
    (
        "W3ExecCensus",
        "executor",
        "Run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root "
        "/home/vgpnk/Projects/shokunin chousa and paste every output line and the exit code.",
    ),
    (
        "W3ExecFileCensus",
        "executor",
        "Run /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "
        f"{LANE}/.ufo/waves/round-44/assimilation/validate/corpus/SOURCES.md and paste the "
        "output and the exit code. This is the validate-before-append mirror. State whether "
        "any E03 or E04 finding appears.",
    ),
    (
        "W3ExecNumstat",
        "executor",
        "Run git -C "
        f"{LANE} diff --numstat 043f19a1db91288947493d9f879e61e7a9f07241..master -- corpus/ tools/ "
        "and paste it. Then list which paths under corpus/ and tools/ are new in this round "
        "and which are modified. Do not commit anything.",
    ),
    (
        "W3ExecShaRfc",
        "executor",
        "Confirm the RFC capture file name d0c4a09a9de32cb91d5e3797.txt equals the first 24 "
        "hex digits of sha256 of the string https://www.rfc-editor.org/rfc/rfc7089.txt. "
        "Paste both values and the command you used. Do not fetch the URL.",
    ),
    (
        "W3ExecWarp",
        "executor",
        "Confirm the string 'National institution websites are archived once per month' is a "
        "contiguous substring of the WARP capture file under "
        "/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/.qcache whose sha256 is "
        "a7e46e274b0784f81426bdc602785b03db1fa87f8f34916097d42ff36cac8dc8, and report the "
        "byte offset. Paste the sha256sum line and the offset. Do not fetch.",
    ),
    (
        "W3ExecE2867",
        "executor",
        "Confirm the token warp.ndl.go.jp/web/20250102112233 appears in the E2867 capture "
        "whose sha256 is "
        "d2a58e70eb8a2b4e42836c0b3df5035c67a45bbce71c412cbcd2bfb155d4848f, and report the "
        "byte offset. Paste the sha256sum line and the offset. Do not fetch.",
    ),
    (
        "W3ExecSelftest",
        "executor",
        "Run the lane's launcher selftest: "
        f"bash {LANE}/tools/parent-lifetime.sh --selftest --receipt "
        "/tmp/w3-selftest-exec.receipt ; paste the receipt content and the exit code. Then "
        "say what the selftest does and does not cover. Do not write inside the lane tree.",
    ),
    (
        "W3ExecErrata",
        "executor",
        "Run python3 "
        f"{LANE}/corpus/evidence/round44/errata-count.py --file "
        f"{LANE}/corpus/evidence/round44/claims.md and paste stdout and the exit code. Then "
        "run the same command against "
        f"{LANE}/corpus/evidence/round44/controls/errata-two.txt and "
        f"{LANE}/corpus/evidence/round44/controls/errata-zero.txt and paste both outputs and "
        "both exit codes. Say what the round's own errata count is.",
    ),
    (
        "W3ScoutConsider",
        "scout",
        "Read "
        f"{LANE}/considerthese/2026-10-24.md and list each proposal it contains with a "
        "one-line description. Then quote the QUALITY.md criterion that carries the one "
        "proposal this round mined, with its line number. Then state whether any other "
        "proposal in that file is still unimplemented and name it. Do not draft a criterion "
        "for another proposal and do not edit the considerthese file.",
    ),
    (
        "W3ScoutFrontier",
        "scout",
        "Read the '## Frontier' section of "
        f"{LANE}/corpus/README.md and the '## Gate' block of "
        f"{LANE}/corpus/lessons/round-44.md. State which coverage-map ground the two new "
        "knowledge entries add that the lane did not hold before this round, quoting the "
        "README lines you rely on. Say whether the round-44 entries are on ground the lane "
        "already held.",
    ),
    (
        "W3ScoutQuar",
        "scout",
        "Find the round-42 adjudication of the chousa slice of the campaign's "
        "absent-defect register under "
        f"{LANE}/corpus/evidence/round42/ and paste the count of rows adjudicated and the "
        "file paths. Then state whether round 44 owes a new per-row quarantine verdict for "
        "the chousa slice, and cite the instruction that decides it.",
    ),
    (
        "W3ScoutAdj",
        "scout",
        "Search every sibling lane repo under /home/vgpnk/Projects/shokunin/*-shokunin/ "
        "for a corpus/SOURCES.md row whose URL contains 'rfc7089' or 'warp.ndl.go.jp'. Report "
        "which lanes already hold the same URL and the row id each one uses. Read only; do "
        "not edit any sibling.",
    ),
    (
        "W3ScribeShonen",
        "scribe",
        "Draft the four SHONEN.md checkbox lines for round 44. Each line must be one of the "
        "four existing boxes, carry a resolvable evidence pointer, and no line may be '[x]' "
        "because promotion is operator-owned. Output the four lines only. Do not edit "
        "SHONEN.md.",
    ),
    (
        "W3ScribeLog",
        "scribe",
        "Draft the LOG.md entry for round 44 in the lane's existing style: one line per "
        "landed change, each with the evidence pointer that motivated it (a file path and "
        "the counter that measured it). Output the entry text only. Do not edit LOG.md.",
    ),
    (
        "W3ScribeScore",
        "scribe",
        "Draft the SCORECARD.md rows for round 44 in the lane's existing style: one row per "
        "claim C1, C2 and C3 carrying the axis, the score delta, the counting command, the "
        "evidence pointer and the measured commit; plus a freshness cell that reads "
        "unchanged rather than improved. Output the rows only. Do not edit SCORECARD.md.",
    ),
    (
        "W3ScribeLesson",
        "scribe",
        "Draft, in the lane's existing style, the '## Spot-check' section and one further "
        f"'## Mistakes' entry for {LANE}/corpus/lessons/round-44.md. The mistake to record: "
        "the wave-2 parent-lifetime receipt was truncated at 5 reap lines and carries no "
        "'end parent_pid=' line because the orchestrator process died before the launcher "
        "finished waiting, so a receipt without that line proves nothing about parent "
        "lifetime. Give the class, the evidence pointer, the captured-by criterion and the "
        "fix. Output the text only; do not edit the lesson file.",
    ),
    (
        "W3ConnIds",
        "connector",
        "Check that every S-id cited anywhere under "
        f"{LANE}/corpus/knowledge/ and in {LANE}/corpus/lessons/round-44.md resolves to a "
        f"row in {LANE}/corpus/SOURCES.md. List every dangling id with its file and line, "
        "and state the total count of distinct ids checked.",
    ),
    (
        "W3ConnUsedby",
        "connector",
        "Check the used-by cell of rows S079, S080 and S081 in "
        f"{LANE}/corpus/SOURCES.md. List exactly which files cite each of the three ids "
        "(grep the lane tree), and say whether the used-by cell names exactly those files "
        "and no others. Paste the three used-by cells and your file lists.",
    ),
    (
        "W3SimpCols",
        "simplifier",
        "Count the columns of each registry row this round added to "
        f"{LANE}/corpus/SOURCES.md (S079, S080, S081) and of the three staged rows in "
        "/home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md they came from. Name "
        "which staged cells had to be rewritten for the lane schema, and quote the before "
        "and after of one such cell. Read only.",
    ),
    (
        "W3SimpIds",
        "simplifier",
        "Show from the lane's own files that lane id S079 is bound to the RFC 7089 URL by "
        f"document, not by arithmetic: quote the URL cell of lane row S079 in "
        f"{LANE}/corpus/SOURCES.md, and quote the staged row id and URL cell for the same "
        "URL in /home/vgpnk/Projects/shokuknow/merge/chousa/SOURCES.append.md. State what "
        "the arithmetic alternative would have produced and why it is wrong.",
    ),
]


def main() -> int:
    directive = DIRECTIVE.read_text(encoding="utf-8").strip()
    items = []
    for name, role, task in ITEMS:
        body = (
            f"/skill:godspeed\n{directive}\n\n{task}\n\n"
            f"Write the report at {WAVE}/{name}.md and nowhere else.\n\n"
            "If the Write tool is unavailable, write that same file with a shell "
            "redirection and no other path. Do not fetch. Do not edit production files. "
            "Do not run jj or git commit."
        )
        items.append(
            {
                "name": name,
                "role": role,
                "item": body,
                "axes": ["operability", "calibration", "depth"],
                "milestone": "Round 44 wave 3: falsify the landed round-44 state",
            }
        )
    spec = {
        "wave": "chousa-r44-w3",
        "milestone": "Round 44 wave 3: falsify the landed round-44 state",
        "reportDir": ".ufo/waves/round-44/w3",
        "axes": ["operability", "calibration", "depth"],
        "context": CONTEXT,
        "items": items,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    roles: dict[str, int] = {}
    for it in items:
        roles[it["role"]] = roles.get(it["role"], 0) + 1
    attack = sum(
        v
        for k, v in roles.items()
        if k in ("reviewer", "critic", "mutation-tester", "revenger", "sentinel")
    )
    print(f"items={len(items)} roles={roles} attack={attack} ({attack / len(items):.1%})")
    print(f"spec={OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
