# R77ScoutA — order-leg source reading (installed bytes only)

Seat: R77ScoutA (scout). Scope: what the round-77 order leg rests on, from the installed Python sources. No network, no repo writes, no installs. Read-only except this report.

## Axes

1. Installed file identity: path, interpreter, digest.
2. (i) Seed determinism of `random.Random(seed).shuffle`.
3. (ii) Unpredictability of `secrets.randbits`.
4. Fit of the order-leg sentence "a fresh seed per run makes the subject order unpredictable to a child process" against those sources.

## Files and digests

- Interpreter: `python3 -VV` → `Python 3.14.8 (main, Oct  2 2026, 10:23:31) [GCC 16.2.1 20260810]`; `sys.executable` → `/usr/bin/python3.14`.
- `python3 -c 'import random,secrets,hashlib; print(random.__file__, secrets.__file__)'` → `/usr/lib/python3.14/random.py /usr/lib/python3.14/secrets.py` (exit 0).
- `sha256sum` (exit 0):
  - `cf8e72f887d838e273c274b79758b2bf8630a0927112b8876fa3a9e4b9b1756b  /usr/lib/python3.14/random.py` (1087 lines)
  - `277000574358a6ecda4bb40e73332ae81a3bc1c8e1fa36f50e5c6a7d4d3f0f17  /usr/lib/python3.14/secrets.py` (71 newline-terminated lines)

## (i) Determinism given a seed — `/usr/lib/python3.14/random.py`

Primary located quote (line 129, `Random.seed` docstring):
> "Initialize internal state from a seed." (7 words)

Supporting located lines:
- L134–135: "None or no argument seeds from current time or from an operating system specific randomness source if available." (no seed → OS/time; this is the non-deterministic branch)
- L137: "If *a* is an int, all bits are used."
- L140–141 (wrapped; scoped to version 1 only): "For version 1 (provided for reproducing random sequences from older versions of Python)" (13 words)
- L173: `super().seed(a)` — an int seed is passed straight to the C base `_random.Random`.
- L177: "Return internal state; can be passed to setstate() later." (`getstate`)
- L356–363, `shuffle`: docstring L357 "Shuffle list x in place, and return None."; body draws only from `randbelow = self._randbelow` (L359) and `j = randbelow(i + 1)` (L362).
- `_randbelow` is bound at L239 / L242 (`_randbelow_with_getrandbits` / `_randbelow_without_getrandbits`) and L274 (module default).

What the file states: a seed initializes internal state (L129), an int seed is used in full (L137), and the shuffle's only random draws go through the instance's `_randbelow` (L359–362).

What the file does not state: no sentence in `random.py` says "same seed, same sequence" for version 2. The only "reproducing random sequences" wording (L140–141) is scoped to version 1. `grep -n -i -E 'same (seed|sequence)'` → no matches. The word "determin" appears once, at L229, about `random()`/`getrandbits()` availability and not about seeds. Determinism for int seeds is therefore an **[INFERENCE]** from the code path (seed → C state → only `_randbelow` draws in `shuffle`). The C module `_random` is not in the installed `.py` files and was not opened.

## (ii) Unpredictability — `/usr/lib/python3.14/secrets.py` (plus `random.py` for the OS backing)

Primary located quote (lines 1–2, module docstring; the sentence wraps across the two lines):
> "Generate cryptographically strong pseudo-random numbers suitable for managing secrets such as account authentication, tokens, and similar." (16 words)

Binding lines:
- L18: `from random import SystemRandom`
- L20: `_sysrand = SystemRandom()`
- L22: `randbits = _sysrand.getrandbits`

Backing source in `/usr/lib/python3.14/random.py`:
- L897–899, `class SystemRandom` docstring: "Alternate random number generator using sources provided by the operating system (such as /dev/urandom on Unix or CryptGenRandom on Windows)." (20 words; wraps at L898–899)
- L910–916, `getrandbits`: docstring L911 "getrandbits(k) -> x.  Generates an int with k random bits."; code L915 `x = int.from_bytes(_urandom(numbytes))`, where `_urandom` is `os.urandom` (`from os import urandom as _urandom`, L57).

What the files state: the generator is described as cryptographically strong (secrets.py L1–2) and drawn from an operating-system source (random.py L898–899, code L915).

What the files do not state: `grep -c -i npredictab` → 0 in both files. "unpredictable" is never written. Neither file says anything about process isolation, a child process, or who can read a seed. The OS-randomness property is code plus a description; the docstrings do not claim unpredictability in any named threat model.

## Does the quote support "a fresh seed per run makes the subject order unpredictable to a child process"?

Partially.

Supported by the sources and battery code:
- The seed is fresh per run. `matrix-battery-v4.py` L177–180 is `for i in range(runs): order = list(subjects); if permute: random.Random(secrets.randbits(64)).shuffle(order)`. The 64-bit seed is drawn inside the per-run loop, and `score()` is called separately for the matrix and for each of the three oracles.
- The seed comes from the OS-backed `SystemRandom` path (secrets.py L20–22; random.py L915).
- The battery prints only `sha256` of the joined order (L181–182) and never prints the seed. The seed is not on argv or in the environment of the child: the child is started at L150 with `[sys.executable, "-B", str(matrix), "--counter", str(subject), ...]`, and L148 adds only `LOADER_MATRIX_CHILD_TIMEOUT` to the environment.

Not supported by the quotes:
- **"unpredictable"**: absent from both files. The quote supports "cryptographically strong", not "unpredictable to any observer".
- **"to a child process"**: no sentence in either file addresses child processes, parent memory, `/proc`, or same-uid visibility. The claim that the child cannot read the seed rests on the battery not passing it (verified in code) and is **not** established by the installed sources. A same-uid child reading the battery's process memory or `/proc/<pid>` would be outside these quotes. **[INFERENCE — not verified; out of installed-source scope.]**
- **Strength of the permutation itself**: `random.Random` is a Mersenne Twister. The module docstring (L40–43) calls it "one of the most extensively tested generators" — a statistical-quality statement, not an unpredictability statement. Thus unpredictability of the order rests entirely on the 64-bit seed being unguessable, not on the MT core. The 64-bit seed space (2^64) exceeds 13! ≈ 6.2×10^9, so the seed space is not the bottleneck; the seed's secrecy is.
- **Enumerability if the digest leaked**: the printed ORDER digest is over one of 13! orderings of fixed names, so a party who saw the digest and the name list could enumerate candidates. The child cannot see the battery's stdout, since the battery captures child output and not the reverse, but this is **[INFERENCE]**, not checked by a probe.

Recommended SOURCES row shape (not written: `corpus/SOURCES.md` is read-only for this seat; planner assigns the id):
- source: Python 3.14 `random` module, installed `/usr/lib/python3.14/random.py`, sha256 `cf8e72f8…1756b`; scope: `Random.seed` and `SystemRandom` behaviour as shipped, not Mersenne Twister security; anchor: L129, L134–135, L137, L140–141 (version-1 scope), L356–363, L897–899, L910–916.
- source: Python 3.14 `secrets` module, installed `/usr/lib/python3.14/secrets.py`, sha256 `27700057…f0f17`; scope: the docstring's "cryptographically strong" description and the `randbits` binding; anchor: L1–2, L18, L20, L22.
- teaches: "A fresh 64-bit `secrets.randbits` seed per run is cryptographically-sourced and drawn from the OS; the shipped docstrings say 'cryptographically strong' and do not say 'unpredictable' or describe process isolation."
- status: `queued` (not admitted without a non-author check); tier A for the scoped docstring statements only.

## Verification record

- Probe 1 (`python3 -` quote-line pinning, first run): exit 1 — my own anchor for the version-1 quote missed the wrapped line; fixed by matching the two wrapped halves. Probe 2: exit 1 — `randbelow = self._randbelow` matched two lines (359, 434); fixed by anchor choice. Probe 3 (final, the reported numbers): exit 0, every anchor asserted unique or expected-count.
- Exact line checks (final bash probe, exit 0): `from os import urandom as _urandom` at random.py L57; battery `env = dict(...)` at L148 and `subprocess.run([sys.executable, "-B", ...` at L150; battery L47 is a docstring mention of the env name.
- Scratch: `/fast/scratch/hyaku/chousa-r77/R77ScoutA` created and removed by an EXIT trap; no files were written there.
- Report integrity: an erroneous `_edit` (a `PUT 1*` placeholder) overwrote this file once; the full report was rewritten from the verified content above. Nothing else in the lane was touched by that call.

## Tools

No tools installed or upgraded. No pacman transaction (host guard in force). No network use.

## Remaining unknowns

- Whether a same-uid child can read the battery's seed through `/proc` or process memory: not checked; outside installed Python source.
- The OS randomness guarantee itself (`os.urandom` / `getrandom(2)` documentation): not opened; a lead for a separate source row.
- The C `_random` Mersenne Twister's seeding and output: not in the installed `.py` files; the "same seed, same sequence" property for version 2 is inferred from code, not quoted.
