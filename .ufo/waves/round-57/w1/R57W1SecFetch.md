# R57W1SecFetch — security review: tools/capture-fetch.py + round-57 egress posture

Seat: security reviewer (UFO-FSD), leaf, no subagents. Lane tip f9736a39; claims frozen
(c2f914c5 / fd95724d). I wrote nothing to the lane/fleet/shokuknow, fetched nothing external
(fixture probes used loopback `127.0.0.1:1` only). Tooling: nothing installed — host python3
3.14.8, curl 8.23.0, pdftotext 26.08.0 (exactly the recipe's pinned version, claims.md:37);
pacman untouched per host guard. Frozen counters/tool not modified; the tool was copied into
scratch for mutation-free behavioral probes.

Axes: A injection surface · B method/egress hygiene · C write confinement · D attempt-cap
integrity · E recipe confinement · F approval-table scope holes. Godskeep pass: cheap probes,
findings reported (frozen items not patched).

## Evidence (commands run)

1. Full static read of `tools/capture-fetch.py` (200 lines). Imports (L37-45): no
   urllib/requests/socket; lone network path is the curl subprocess. `grep shell=True` → no match.
2. `python3 tools/capture-fetch.py --status` (read-only; no writes on this path): pairs=62→66,
   rows=114→118 during my window — L1 C3 scouting in flight. Pending C2 retries: S100/S103/S106
   at attempts=2 fails=1; S105 attempts=3 fails=3 (cap reached).
3. Scratch fixture (`$HYAKU_SCRATCH/fixture{,-scratch}`, tool copied, fake refetch.tsv):
   a) saturated (id,url) → `FAKE … already 3 attempts (max 3) — skipped`, exit=0, row count
   unchanged (refusal path, L192-194).
   b) same URL under alias id OTHER → `attempt=1 rc=7 http=000` executed (cap keyed by (id,url), L182).
   c) `--url=-V` → curl parsed `-V` as its own flag: rc=0, http field holds the multi-line
   version banner → malformed multi-line row appended to refetch.tsv (no `--` separator, no
   numeric validation of http, L127-143).
   d) failure run left `corpus/captures/` empty; only `fixture-scratch/.../refetch.append` created.
4. In-lane check: `awk` over refetch.tsv — 52 URLs repeat across rows but **0** URLs map to >1
   distinct id → per-(id,url) cap ≡ per-URL cap in current data.
5. `ls ~/.curlrc` → absent. `pdftotext -v` → 26.08.0.

## Findings (severity order)

- **F1 MEDIUM — "L1 only" is policy-only; the tool has no caller gate.** `main()` fetches for
  any invocation (L190-195); a successful rogue run overwrites `corpus/captures/<key>.raw`
  (L117-119) and appends a refetch.tsv row (L114-116), and the frozen counter takes the LAST
  successful row (tool docstring L15; claims.md:31) → a compromised seat could flip canonical
  C2 bytes. Mitigations (residual risk, not a fix): seats cannot commit (host guard), so rogue
  writes surface as a dirty tree the L1's before/after receipts catch; predicate recomputes from
  committed bytes (claims.md:20-22); every row auditable. Reported, not patched.
- **F2 LOW — argv flag-smuggling + unvalidated http field.** URL is the last argv element with
  no `--` (L127-128); probe (c) shows a `-`-leading URL is consumed as a curl option and writes
  a schema-breaking multi-line row. Latent: manifest-pinned URLs don't start with `-`; freeze-bound.
- **F3 LOW — curl runs without `-q/--disable`:** curl 8.x reads `~/.curlrc` by default; a
  same-uid write there could inject additive options (headers) into campaign fetches. Absent
  today (check 5). Defense-in-depth; freeze-bound.
- **F4 INFO — cap key vs table wording.** Tool caps per (id,url) (L182,L191-194); egress table
  line 14 caps "per URL". Probe (b) resets the budget under an alias id; check 4 shows 0 such
  URLs in-round, so the caps coincide in practice. Latent only.
- **F5 INFO — TOCTOU on the cap:** read_records→append (L177-182 vs L106-121) has no lock;
  two concurrent L1 passes could interleave rows and overshoot. Unexercised this round.
- **F6 INFO — dead weight:** `code_file` built but never used (L126,L149); `tempfile` imported
  unused (L45, grep-confirmed); scratch mirror `refetch.append` written, never read (L111-113).
- **F7 INFO — PATH-resolved binaries** (`curl` L127, `pdftotext` L83); absolute paths would be
  firmer. Out-of-model (PATH host-owned).

## Required checks (all PASS)

1. **No injection surface:** argv list, no shell=True (L127-130); grep confirms.
2. **Method:** only `-fsSL --compressed --max-time 15 -A <UA> -o -w %{http_code}` (L127-128) —
   GET implied, no -d/-X/-b/-c/-u/--netrc anywhere; UA = campaign UA (L55-56); wrap timeout 25 s
   + --max-time 15 (L130,L127).
3. **Write confinement:** STORE/REC/EVID are lane store+evidence (L49-51); curl temp + mirror +
   recipe under `$HYAKU_SCRATCH/chousa-r57/fetch` (L183-185, L111, L125); probe (d) confirms
   store untouched on failure.
4. **No /tmp:** `tempfile` unused (L45); default scratch `/fast/scratch/hyaku` (L24,L183).
5. **Refusal >3 attempts:** MAX_ATTEMPTS=3 (L54); saturated pair prints skip and continues,
   exit 0, no row (probe (a); L192-194).
6. **pdftotext on scratch bytes only:** `r.pdf` written into the scratch `recipe/` dir, stdout
   captured, file unlinked (L79-88); probe shows leftover=[]; host version 26.08.0 = pinned.

## Egress table review (egress-approval.md)

- **T1 LOW — Row 4 (L17) ambiguity:** its "not allowed" column lists only store writes; whether
  row 1's prohibitions (L14: POST/cookies/credentials/>3 attempts) bind seat re-opens rests on
  "as the first row" in the method column. A compromised seat could argue POST or uncapped
  re-opens are permitted. Clarify next round. (My item named no URL → I performed no re-open.)
- **T2 LOW — redirect scope:** `-L` is inside the frozen recipe (L127, L14), so a named URL may
  30x to any host incl. internal/loopback; for row-4 fetches that is SSRF-by-redirect into seat
  scratch. Impact bounded: canonical store is seat-immutable, exfil channel capped at the
  ≤120-line report, probes auditable via the naming requirement.
- **T3 INFO — search row (L16):** purpose-bound to locating R57-C3 documents; the record duty
  (query+URL in lesson `## Gate`) binds the L1's lesson, not a compromised seat's off-purpose
  queries, which fall to default-deny (L19) but are unrecorded. Bandwidth = query strings.
- **Positive:** default-deny closure (L19), fixed method/UA/attempt cap, per-attempt record, and
  committed content-addressed bytes give C2/C3 evidence seat-immutability in practice (mod F1).

## Residual risk / verification gaps

F1 is the live exposure (policy-only L1 gating); bounded by the no-commit guard + receipts.
Did not diff the tool against its cited shokuknow origin (frozen provenance, docstring L4-5,
sha256 e864a01f…). F5 untested (no concurrent runs). All other findings latent/INFO.

Scratch `/fast/scratch/hyaku/chousa-r57/R57W1SecFetch` deleted (`rm -rf`, verified — no
R57W1SecFetch entry remains under chousa-r57/).

VERDICT: attacked the capture-fetch tool's injection/egress/confinement posture and the round-57
approval table — required controls (argv-only curl, GET recipe, store/scratch confinement, no
/tmp, 3-attempt refusal, scratch-only pdftotext 26.08.0) all survived probes; one MEDIUM
(policy-only L1 gate, F1), three LOW (F2 flag-smuggle, F3 .curlrc, T1/T2 table scope holes),
rest INFO. Nothing patched (frozen); reported per protocol.
