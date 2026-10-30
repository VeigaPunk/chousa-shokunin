# Draft10 — SOURCES contract/schema review and draft block

## Behavior and axes

Axes: schema fidelity, provenance precision, rejection completeness, frozen-claim honesty. Read-only review; the block below is a draft for L1, not an admission, production edit, or outside non-author closure. No runtime, probe, clone, network access, git/jj command, package installation, or service operation was invoked. Scratch was not created, so none remains.

## Contract and findings

Authoritative schema: fleet `.ufo/waves/kaika/SOURCES-CONTRACT-v1.md:19–50,59–61` (read at snapshot CBCA). Eleven cells; next unused S-id; no literal pipe within a cell; allowed kinds include `code`, `docs`, `own-work`; scoped A/B/C; exact anchor plus revision; ISO opening date; cadence; mined rows cite an existing entry through `used-by`. Rejection syntax is `REJECTED: <reason>; flip: <what would change the verdict>`. Corrections to immutable cells require a new superseding row, not an in-place rewrite.

Observed current registry: `corpus/SOURCES.md:160–163` already contains S150–S153 (snapshot 8D3E). Therefore **do not append those IDs again**. The draft below represents the proposed four-row block only; L1 must reconcile it with its already-present working rows. If those rows are already committed, changed source/anchor/teaches cells require new IDs with `supersedes S150 —` etc. No registry mutation or census was performed here.

- S150: `code` / A is permitted and appropriate for the installed implementation, not repository identity. Direct read of `/usr/lib/python3.14/pathlib/__init__.py:49–72,392–396,932–938` confirms the cited logical-parent docstring, positional slice, `strict=False`, and realpath delegation. The version 3.14.8 is inherited from L1's row, not independently executed here.
- S151: `docs` / A is structurally valid for GNU realpath's own option. This seat did not reopen or render the compressed manual and does not certify its quote, version, or opening receipt. L1's lesson Gate records the local location and quote. Preserve that provenance distinction.
- S152: `own-work` / B is conservative and schema-valid for written code. Direct read of `c3-count.py:34–39,85–93` confirms the startup check and independent expected-path expression. It is **not the probe output proposed by frozen C3**; `claims-erratum.md:9` and `lessons/round-64.md:19` disclose that substitution. Source-code admission cannot prove the frozen execution target.
- S153: `own-work` / C / rejected with `used-by = —` correctly retains a refused candidate and explicit flip. Direct read confirms the G02 sentence at candidate line 18. The flip asks for different evidence; it does not turn the docstring itself into execution evidence. Candidate `ref-preflight-v3.py` is not production.
- The current four rows have eleven cells by inspection, allowed enums, ISO dates, a cadence, and no embedded cell pipes. This is manual schema review, not validator execution.
- `corpus/knowledge/lane-root-derivation-r64.md` explicitly cites S150–S152 and its claims label inference/observation. The lesson's `## Gate` contains all four located quotes, a shared access date, three admits and one reject. This seat does not claim those access attestations are independently byte-receipted; QUALITY 57 requires durable access evidence.
- Search-log coverage is separate: the inspected `SOURCES.md` Search log has no Round64 entry. A new-row block alone does not satisfy contract rule 5. A draft note is supplied below; it must not claim this seat opened the manual.

## Draft registry block — not an append instruction

Use only if these rows are not yet integrated. They already appear in the observed working registry. Source/version/opening attestations below remain L1's, not execution evidence from this seat.

```markdown
| S150 | pathlib installed Python source — /usr/lib/python3.14/pathlib/__init__.py, Python 3.14.8 | code | A | positional logical parents and Path.resolve implementation in the installed Python; not intended repository identity | _PathParents.__getitem__ lines 63–72; PurePath.parents lines 392–396; Path.resolve lines 932–938, installed Python 3.14.8 | parent indexing removes path components positionally; resolve delegates to os.path.realpath with strict defaulting false | mined | 2026-10-30 | on-release | corpus/knowledge/lane-root-derivation-r64.md |
| S151 | realpath(1) — installed /usr/share/man/man1/realpath.1.gz, GNU coreutils 9.12, September 2026 | docs | A | GNU realpath existing-components option; not Python default behavior or repository identity | DESCRIPTION -e --canonicalize-existing, coreutils 9.12, September 2026 | requiring existing components is an explicit mode, not evidence of an intended lane root | mined | 2026-10-30 | on-release | corpus/knowledge/lane-root-derivation-r64.md |
| S152 | Round64 relocation counter source — corpus/evidence/round64/c3-count.py | own-work | B | the counter's written startup assertion and expected-path arithmetic; not execution results or a passing relocation verdict | startup lines 34–39 and relocation loop lines 85–93, frozen round64 c3-count.py sha256 prefix 465a8c5efbb870f7 | the written check names a missing derived file before measurement; the independently written relocation expectation does not prove its own correctness | mined | 2026-10-30 | on-release | corpus/knowledge/lane-root-derivation-r64.md |
| S153 | Candidate preflight docstring — corpus/evidence/round64/controls/ref-preflight-v3.py | own-work | C | stated knowledge-index contract as evidence of implementation correctness | module docstring Gates G02 line 18, inherited round64 candidate read 2026-10-30; not production | REJECTED: the docstring states intent and the candidate needs behavioral checks; flip: use executed fixtures discriminating the asserted behavior as a separate evidence source instead | rejected | 2026-10-30 | on-release | — |
```

S153's draft anchor still lacks an independently recorded candidate revision/digest: a reading date is not a byte revision. L1 must bind that candidate snapshot before admission; no digest is invented here. S150/S151 versions and S152 frozen digest are inherited locators, not checks performed by this seat.

## Draft Search log note — conditional on L1's opening evidence

```markdown
- Round64 (2026-10-30): question — what do positional ancestry, normalization and explicit existence checks establish about a research instrument's derived lane path? Where: installed Python pathlib source, installed realpath(1) manual, frozen c3-count.py source and inherited candidate preflight docstring; no network. Identified 4 candidate sources, screened 4, included 3 as S150–S152, excluded 1 as S153 because stated intent is not behavioral evidence (flip retained in the row). Stop rationale: these sources ground the entry's narrow code/option distinctions; counter execution and intended-root identity remain separate. S152 records counter code, not the probe-output source originally proposed by frozen C3. Opening attestations and located quotes are in corpus/lessons/round-64.md ## Gate; frozen claim outcomes are not inferred from source admission.
```

## Gates and known limits

No checks were run: there are no command outputs or process exit codes to report. Tool reads succeeded; they do not establish a CLI PASS. Frozen C1's E12/E13 mismatch remains a failure of the frozen full-pass target, as recorded in `claims-erratum.md:5`; the distinct `c1-battery-supplement.py` cannot replace it. C3 source substitution and counter arithmetic limits remain explicit. Claims/counters/operator inputs were not edited.

For L1 only, prospective checks (NOT RUN here): registry validator `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md`; check new source access receipts, candidate revision binding, and final used-by backlinks. No proposed command here is execution evidence.

## Touched surfaces, provenance and conflicts

Written surfaces: `.ufo/waves/round-64/w1/Draft10/report.md` and the explicitly requested trailer report `.ufo/waves/round-64/w1/Draft10.md`. Production surfaces unchanged by this seat. Tools installed/updated: none.

Key reads: mandatory host RULES; frozen `corpus/evidence/round64/claims.md` (CC2B); SOURCES contract (CBCA); `corpus/SOURCES.md` (8D3E); QUALITY criteria 6–8, 13, 57; round64 lesson (9F1A), entry (C55E), erratum (E698), counter (D924), candidate (53A6), installed pathlib (C299). Exact tool selectors and returned excerpts remain in this seat's transcript. Read/grep/glob only; no command was executed to decorate this report.

Assignment path conflict retained verbatim: “Write only your own report and evidence beneath /home/vgpnk/Projects/shokunin/chousa-shokunin/.ufo/waves/round-64/w1/Draft10/ (report.md)” versus “Report: write your scoped findings to .ufo/waves/round-64/w1/Draft10.md”. Both explicitly named report paths are supplied; the trailer path is a pointer to this complete report. This is a reporting conflict for the canonical Rust judge, not an attempt to alter authorization.

Out of scope: production integration, source census execution, fresh quote probes, frozen counters, fixture repair, scores, non-author closure, commits/pushes, runtime dispatch.

## Self-evaluation

Accuracy 4/5: distinguishes direct reads from inherited manual/version attestations; manual opening is not independently checked. Completeness 4/5: registry and Search log drafts supplied; final candidate revision must come from L1's real snapshot. Clarity 4/5: explicit duplicate-ID warning, though two requested report paths require a pointer. Actionability 4/5: usable draft and prospective gate named; intentionally not integrated. Conciseness 4/5: provenance detail is longer than the four-row draft. Overall 4.0/5. Improvements: bind S153 to its actual revision; attach existing opening receipts rather than rerun work; reconcile already-present rows under append-only rules. Self-check: assessment matches this seat's draft-only remit, not admission or claim closure.
