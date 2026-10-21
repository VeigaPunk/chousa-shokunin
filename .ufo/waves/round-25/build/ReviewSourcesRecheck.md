# Round-25 source recheck

As of **2026-10-21**. Registry contract: `CORPUS.md` lines 105–106 defines `recheck` as ISO date or cadence (`90d`, `180d`, `on-release`). Axes: freshness; event-triggered means no calendar deadline, not proof that all release events were checked.

## Census command and result

Command run against `corpus/SOURCES.md` (dated cadences calculated from each row's `opened` date; `on-release` is event-triggered):

```sh
TZ=UTC LC_ALL=C awk -F'|' -v asof=2026-10-21 '
function trim(s) { sub(/^[[:space:]]+/, "", s); sub(/[[:space:]]+$/, "", s); return s }
BEGIN { split(asof, a, "-"); asof_ts=mktime(sprintf("%04d %02d %02d 00 00 00", a[1], a[2], a[3])) }
/^\| S[0-9][0-9][0-9] / {
  id=trim($2); opened=trim($10); cadence=trim($11)
  split(opened, d, "-"); opened_ts=mktime(sprintf("%04d %02d %02d 00 00 00", d[1], d[2], d[3]))
  if (cadence ~ /^[0-9]+d$/) {
    days=cadence; sub(/d$/, "", days); due_ts=opened_ts+days*86400
    printf "%s opened=%s recheck=%s due=%s deadline=%s\n", id, opened, cadence, (asof_ts>=due_ts ? "yes" : "no"), strftime("%Y-%m-%d", due_ts)
  } else if (cadence == "on-release") {
    printf "%s opened=%s recheck=%s due=event-triggered (no calendar deadline)\n", id, opened, cadence
  }
}' /home/vgpnk/Projects/shokunin/chousa-shokunin/corpus/SOURCES.md
```

Observed output:

```text
S001 opened=2026-10-19 recheck=on-release due=event-triggered (no calendar deadline)
S002 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S003 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S004 opened=2026-10-19 recheck=on-release due=event-triggered (no calendar deadline)
S005 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S006 opened=2026-10-19 recheck=90d due=no deadline=2027-01-17
S007 opened=2026-10-19 recheck=90d due=no deadline=2027-01-17
S008 opened=2026-10-19 recheck=on-release due=event-triggered (no calendar deadline)
S009 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S010 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S011 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S012 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S013 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S014 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S015 opened=2026-10-19 recheck=90d due=no deadline=2027-01-17
S016 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
S017 opened=2026-10-19 recheck=on-release due=event-triggered (no calendar deadline)
S018 opened=2026-10-19 recheck=365d due=no deadline=2027-10-19
```

Thus none of the 14 calendar-cadenced rows are due; S001, S004, S008 and S017 are event-triggered, so the command does not assert their source-release status. S006/S007 were checked below; no newer versions appear.

## Targeted re-open (registry rows `SOURCES.md:16–17`; Gate `corpus/lessons/round-24.md:53–54`)

- **S006 — changed (Gate quote/location check fails; version unchanged).** [arXiv abs](https://arxiv.org/abs/2605.06635) submission history lists only **v1**, 7 May 2026; no newer version. The Gate attributes its phrase to §3.3, but that section gives separate formulations: §3.3.1 “Link Works assesses URL accessibility without LLM inference”; §3.3.2 “Relevant Content measures topical alignment between the claim and the cited source”; §3.3.3 “Fact Check verifies whether specific factual claims are accurately supported by the source content.” The Gate wording does not occur verbatim there. The same concepts appear in the abstract as “(1) Link Works verifies URL accessibility, (2) Relevant Content measures topical alignment, and (3) Fact Check validates factual accuracy against source content” — with numbered insertions, not the unbroken Gate quote. The recorded §3.3 quote is therefore not verbatim at its stated location.
- **S007 — unchanged.** [arXiv abs](https://arxiv.org/abs/2601.08536) submission history lists v1 (13 Jan), v2 (30 Jan), and v3 (10 Sep 2026), with **v3 latest** and no newer version. The Gate quote is an exact substring in current §2.1: “this only measures the accuracy of the citations and does not necessarily confirm that the information is correct”.

No tools installed or updated.
