# Attack04 seat folder

Canonical report: `../Attack04.md` (operator trailer path) — single authority, do not fork.
Seat evidence (uniquely named): `attack04-probe-results.json`, `attack04-p1..p11-*.receipt`, `attack04-counter-run.txt`.

Headline: frozen `no-revision` case is robust (7/7 nearby header mutations rejected), but the
frozen reference validator accepts 4 nearby malformed/forged receipts (doubled separator,
NUL-only body, forged body, concatenated receipt tail) that no frozen counter case covers;
frozen counter still awards 20/20 to a validator showing all four laxnesses. No provenance
break — digest always binds the named blob at the pinned revision; forgery acceptance is a
declared non-goal. No C1 scoring change requested; smallest safe correction is optional
target-side strictness only, zero frozen-byte changes.
