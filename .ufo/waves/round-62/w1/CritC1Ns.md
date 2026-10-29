# CritC1Ns — R62-C1 sandbox-detection attack (critic, w1)

VERDICT: NS_FORGER_ACCEPTED=yes best=20/20

Scope: attack R62-C1 by letting a forger detect the PID namespace. Frozen files read, never edited:
`corpus/evidence/round62/c1v2-count.py` (sha prefix b7016fba91b03460), `c1v2-battery.py`, `controls/`, `tools/build-spans.py`
(prefix c366492005ce304a). Scratch `/fast/scratch/hyaku/chousa-r62/CritC1Ns/` (deleted before yield). No installs, no git mutation.
`best=k/20` = the highest LEGS a forger reached across the three seeds.

## Findings

1. **v2 accepts PID-namespace-detecting forgers.** Forger NSCOMBO (sniff below) reads `LEGS=20/20 C1V2=PASS`, counter exit 0,
   at seeds 1001, 2002, 3003 (a MISS: the forger must exit 1). NSA (`getpid()==1` alone) and NSC (`/proc/1/cmdline` equal to own
   `/proc/self/cmdline`) are also accepted 20/20 at all three seeds. This is the named limit in the claims, now measured.
   - Why: the counter's `unshare -Ufp --kill-child --mount-proc` makes the builder PID 1 (verified: `unshare -Ufp ... python3 -c
     'os.getpid()'` prints `pid 1`). The forger runs the landed builder when it sees that, and the unhardened base otherwise.
     Every leg runs in the sandbox, so every leg takes the honest path.

2. **The claim's example test (`NSpid` with two or more ids) does not fire inside the sandbox.** Forger NSB reads
   `LEGS=9/20`, `11/20`, `11/20` (FAIL, exit 1 at all seeds). Reason, observed:
   `unshare -Ufp --kill-child --mount-proc sh -c 'grep NSpid /proc/self/status; echo pid=$$'` prints `NSpid:	2` and `pid=1`.
   A reader sees only the namespaces at or below its own, so inside the sandbox NSpid has one id. The named example therefore
   is not a working self-detector. The working in-sandbox signals are `getpid()==1` and the `/proc/1/cmdline` match (NSA, NSC).
   The claim text should say so when routed as a limit.

3. **A mountinfo threshold is not a sandbox signal (NSD).** NSD (`len(mountinfo lines) < 40`) reads 20/20 at all seeds, but
   the host itself has 35 lines (`grep -c . /proc/self/mountinfo`), so NSD takes the landed path everywhere. It is honest on every
   host, not a forger. It is excluded from the count of forgers; it shows only that a threshold sniff cannot be the test.

4. **Smallest counter changes (mutant copies in scratch; the frozen counter is untouched).** Both were checked against the
   forgers and against the honest builders:
   - **M1 shim init.** SANDBOX gains a shim so the builder is PID 2:
     `SANDBOX = ["unshare", "-Ufp", "--kill-child", "--mount-proc", "sh", "-c", '"$@" & wait $!; exit $?', "shim"]`.
     Result: NSCOMBO `LEGS=10/20`, `10/20`, `10/20` (FAIL); NSA `11/20` and NSC `9/20` (seed unset, random). Landed
     `LEGS=20/20 C1V2=PASS`; positives pos-ref and pos-indep1..3 each `20/20 PASS` (seed unset). NSD still `20/20`
     (finding 3). The shim alone does not stop an NSpid-style test, but NSpid was already non-functional (finding 2).
   - **M3 no-PID-namespace neutral profile.** Only the neutral profile drops the PID namespace; plain stays as it is:
     `argv = (SANDBOX if fx.profile != "neutral" else ["unshare", "-Uf", "--kill-child"]) + [...]`.
     Result: NSCOMBO `LEGS=11/20`, `10/20`, `11/20` (FAIL); NSA `11/20`, NSC `10/20` (seed unset). Landed `20/20 PASS` and
     positives `20/20 PASS` (seed unset). Mechanism: a forger keyed on the sandbox must run the honest builder in both
     profiles, and it cannot tell the profiles apart without detecting the counter itself. This is the change I would route.
   - Not tested: random pid values (the kernel assigns them; padding them is what M1 does, so this is INFERENCE); M3's effect on
     the sandbox-sensitive forgers F06/F10 and the X02 control (not run; a next-round check); M1 and M3 at three seeds for the
     honest builders (only NSCOMBO was run at three seeds).

5. **Battery reference.** The frozen battery takes no subject of mine (its `--only` selects only its own names). I ran:
   - `python3 -B corpus/evidence/round62/c1v2-battery.py --counter corpus/evidence/round62/c1v2-count.py --work <scratch>/b/frozen-only --only F01`
     → `SUBJECT FORGER F01 ... counter_exit=1 want=1 ok | LEGS=11/20 C1V2=FAIL`, then `FORGERS_REJECTED=1/1 ... BATTERY=FAIL`, exit 1.
   - A scratch copy `battery-ns.py` (paths made absolute, five NS subjects added to SNIFFS; the frozen battery untouched), full run:
     `LANDED=3/3 POSITIVES=4/4 FORGERS_REJECTED=13/17 STUBS_REJECTED=4/4 BATTERY=FAIL` — the misses are NSA, NSC, NSD and
     NSCOMBO (exit 0); NSB is rejected. With the twelve frozen forgers all rejected, the battery reads 12/12 on its own
     subjects. The four NS misses are the open limit in the claims.

## Forger sniffs (the one line each, inside the battery TEMPLATE; the test sets `hit`, the landed builder runs on hit)

- NSA: `hit = os.getpid() == 1`
- NSB: `hit = any(l.startswith("NSpid:") and len(l.split()) >= 3 for l in open("/proc/self/status"))`
- NSC: `hit = open("/proc/1/cmdline", "rb").read() == open("/proc/self/cmdline", "rb").read()`
- NSD: `hit = len(open("/proc/self/mountinfo").read().splitlines()) < 40`
- NSCOMBO: `hit = os.getpid() == 1 or <NSB test> or <NSC test>`

## Evidence pointers (commands run; outputs as observed)

- `python3 -B .../c1v2-count.py --builder <S>/forgers/NSA.py --work <S>/w/NSA-<seed>` with `C1V2_SEED` 1001, 2002, 3003 →
  `LEGS=20/20 C1V2=PASS exit=0` at each seed. NSC and NSCOMBO the same; NSD the same (see finding 3).
- NSB at the same three seeds → `LEGS=9/20 C1V2=FAIL exit=1`, `11/20`, `11/20`.
- `c1v2-count.py` builder sha256 for NSCOMBO: the battery and counter print it per run (`BUILDER sha256=...`).
- Mutant runs: `python3 -B <S>/mut/m1-shim.py ...` and `<S>/mut/m3-nopid-neutral.py ...` on the forgers and the honest builders:
  as in finding 4.
- Battery reference: as in finding 5.

## Calibration and limits

- Measured: NSA, NSC and NSCOMBO are accepted at three seeds each (9 of 9 MISS at 20/20). NSB and NSD are not forgers that
  bite (NSB is broken, NSD is honest everywhere).
- Not measured: M1 and M3 at three seeds on the honest builders; the effect of M3 on F06, F10 and the X02 control; any
  forger that runs a real 192 MiB read in a helper. The forgers were authored by this seat, so the overfit risk named in the claims
  applies to them too.
- The counter was not changed. The mutants are suggestions for the next round's battery, as the claims route post-freeze
  forgers. They are not a refutation of C1 under the frozen rule (`BATTERY=PASS` is decided by the frozen counter).

## Hand-off

- Route to L1: the NS limit is real (NSA, NSC, NSCOMBO accepted); the claim's NSpid example should be replaced with
  `getpid()==1` and the `/proc/1` cmdline match; M3 (no PID namespace in one profile) is the candidate change for round 63.
- Scratch `/fast/scratch/hyaku/chousa-r62/CritC1Ns/` removed before yield.
